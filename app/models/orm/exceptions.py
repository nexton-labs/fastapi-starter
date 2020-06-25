class RecordNotUnique(Exception):
    pass


class RecordNotFound(Exception):
    def __init__(self, model, model_id):
        self.model_name = model.__name__
        self.model_id = model_id
        self.message = (
            f"{self.model_name} not found with id={str(self.model_id).lower()}"
        )


class UnknownCRUDError(Exception):
    pass
