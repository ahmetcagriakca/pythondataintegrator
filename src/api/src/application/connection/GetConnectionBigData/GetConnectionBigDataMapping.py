from typing import List

from pdip.integrator.connection.domain.authentication.type import AuthenticationTypes

from src.application.connection.GetConnectionBigData.GetConnectionBigDataDto import GetConnectionBigDataDto, \
    GetConnectionTypeDto, \
    GetConnectorTypeDto, GetAuthenticationTypeDto
from src.domain.connection.Connection import Connection
from src.domain.secret import SecretSource


class GetConnectionBigDataMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionBigDataDto:
        dto = GetConnectionBigDataDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectionType = GetConnectionTypeDto(Id=entity.ConnectionType.Id, Name=entity.ConnectionType.Name)
        dto.Host = entity.ConnectionServers[0].Host
        dto.Port = entity.ConnectionServers[0].Port
        dto.CreationDate = entity.CreationDate
        dto.IsDeleted = entity.IsDeleted

        dto.ConnectorType = GetConnectorTypeDto(Id=entity.BigData.ConnectorType.Id,
                                                Name=entity.BigData.ConnectorType.Name,
                                                ConnectionTypeId=entity.BigData.ConnectorType.ConnectionTypeId)
        dto.DatabaseName = entity.BigData.DatabaseName
        dto.Ssl = entity.BigData.Ssl
        dto.UseOnlySspi = entity.BigData.UseOnlySspi
        secret_source: SecretSource = entity.ConnectionSecrets[0].Secret.SecretSources[0]
        dto.AuthenticationType = GetAuthenticationTypeDto(Id=secret_source.AuthenticationType.Id,
                                                          Name=secret_source.AuthenticationType.Name)

        if AuthenticationTypes(secret_source.AuthenticationType.Id) == AuthenticationTypes.Kerberos:
            dto.KrbRealm = secret_source.SecretSourceKerberosAuthentications[0].KrbRealm
            dto.KrbFqdn = secret_source.SecretSourceKerberosAuthentications[0].KrbFqdn
            dto.KrbServiceName = secret_source.SecretSourceKerberosAuthentications[0].KrbServiceName

        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionBigDataDto]:
        result: List[GetConnectionBigDataDto] = []
        for entity in entities:
            dto = GetConnectionBigDataMapping.to_dto(entity=entity)
            result.append(dto)
        return result
