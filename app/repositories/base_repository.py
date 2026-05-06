from typing import Generic, List, Optional, Type, TypeVar
from app.extensions import db

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
        db.session.flush()  # ID ataması için, commit service katmanında yapılır
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
