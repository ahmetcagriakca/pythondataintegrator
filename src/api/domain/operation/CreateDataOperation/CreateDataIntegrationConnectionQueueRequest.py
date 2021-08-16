from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CreateDataIntegrationConnectionQueueRequest:
    TopicName: str = None
