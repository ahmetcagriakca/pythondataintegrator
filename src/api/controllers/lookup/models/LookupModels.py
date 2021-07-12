from IocManager import IocManager


class LookupModels:
    ns = IocManager.api.namespace('Lookup', description='Connection endpoints', path='/api/Lookup')
