from domain.common.decorators.requestclass import requestclass


@requestclass
class CreateDataIntegrationConnectionQueueRequest:
    TopicName: str = None
