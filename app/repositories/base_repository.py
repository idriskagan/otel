from typing import Generic, List, Optional, Type, TypeVar
from app.extensions import db
from app.utils.agent_debug import agent_debug_log

T = TypeVar('T', bound=db.Model)


class BaseRepository(Generic[T]):
    """
    Generic CRUD Repository — tüm entity repository'lerinin taban sınıfı.
    Repository katmanı: sadece DB operasyonları burada, iş mantığı Service'te.
    """

    def __init__(self, model: Type[T]):
        self.model = model

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """ID'ye göre tek kayıt döndürür."""
        return db.session.get(self.model, entity_id)

    def get_all(self) -> List[T]:
        """Tüm kayıtları döndürür."""
        return db.session.execute(db.select(self.model)).scalars().all()

    def create(self, **kwargs) -> T:
        """Yeni kayıt oluşturur ve DB'ye ekler."""
        entity = self.model(**kwargs)
        db.session.add(entity)
        # region agent log
        agent_debug_log(
            run_id='register-debug',
            hypothesis_id='H1',
            location='app/repositories/base_repository.py:31',
            message='before flush in create',
            data={
                'model': self.model.__name__,
                'has_password_hash': 'password_hash' in kwargs,
                'password_hash_is_none': kwargs.get('password_hash') is None if 'password_hash' in kwargs else True,
                'keys': sorted(list(kwargs.keys())),
            },
        )
        # endregion
        db.session.flush()  # ID ataması için, commit service katmanında yapılır
        # region agent log
        agent_debug_log(
            run_id='register-debug',
            hypothesis_id='H1',
            location='app/repositories/base_repository.py:43',
            message='after flush in create',
            data={'model': self.model.__name__, 'entity_id': getattr(entity, 'id', None)},
        )
        # endregion
        return entity

    def update(self, entity: T, **kwargs) -> T:
        """Var olan kaydı günceller."""
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        db.session.flush()
        return entity

    def delete(self, entity: T) -> None:
        """Kaydı siler."""
        db.session.delete(entity)
        db.session.flush()

    def save(self, entity: T) -> T:
        """Kaydı DB oturumuna ekler (commit service'te yapılır)."""
        db.session.add(entity)
        db.session.flush()
        return entity

    def commit(self) -> None:
        """Transaction'ı commit eder — genellikle service katmanı çağırır."""
        db.session.commit()

    def rollback(self) -> None:
        """Transaction'ı geri alır."""
        db.session.rollback()

    def paginate(self, page: int = 1, per_page: int = 12, query=None):
        """Sayfalama desteği."""
        if query is None:
            query = db.select(self.model)
        return db.paginate(query, page=page, per_page=per_page, error_out=False)
