from sqlalchemy import select

from fast_zero.models import Todo, User


def test_create_user(session):
    user = User(
        username='testuser', password='testesecret', email='test@test.com'
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'test@test.com'))
    assert result.username == 'testuser'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
