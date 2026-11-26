from sqlalchemy.orm import Session

from app.errors import NotFoundError
from app.repositories.base import BaseRepository, ModelT


def list_entities(session: Session, model: type[ModelT]) -> list[ModelT]:
    return BaseRepository(session, model).list()


def get_entity(session: Session, model: type[ModelT], entity_id: str) -> ModelT:
    entity = BaseRepository(session, model).get(entity_id)
    if entity is None:
        raise NotFoundError(model.__name__, entity_id)
    return entity


def create_entity(session: Session, model: type[ModelT], data: dict) -> ModelT:
    return BaseRepository(session, model).add(model(**data))


def update_entity(session: Session, model: type[ModelT], entity_id: str, changes: dict) -> ModelT:
    repo = BaseRepository(session, model)
    entity = repo.get(entity_id)
    if entity is None:
        raise NotFoundError(model.__name__, entity_id)
    return repo.update(entity, changes)


def delete_entity(session: Session, model: type[ModelT], entity_id: str) -> None:
    repo = BaseRepository(session, model)
    entity = repo.get(entity_id)
    if entity is None:
        raise NotFoundError(model.__name__, entity_id)
    repo.delete(entity)

    # lazy import: avoids a circular import with link_service, which imports this module
    from app.services import link_service

    kind = link_service.MODEL_KINDS.get(model)
    if kind is not None:
        link_service.delete_links_for(session, kind, entity_id)
