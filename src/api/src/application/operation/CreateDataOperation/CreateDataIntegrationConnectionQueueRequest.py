from pdip.cqrs.decorators import requestclass


@requestclass
class CreateDataIntegrationConnectionQueueRequest:
    TopicName: str = None
