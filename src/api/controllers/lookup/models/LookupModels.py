from IocManager import IocManager


class LookupModels:
    ns = IocManager.api.namespace('Lookup', description='Lookup endpoints', path='/api/Lookup')
