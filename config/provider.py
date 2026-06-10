from auth.infrastructure.repositories.user_repo_impl import UserRepoImpl
from auth.infrastructure.repositories.token_repo_impl import TokenRepoImpl
from config.database import get_session
from fastapi import Depends
from messages.infrastructure.repositories.message_repo_impl import MessageRepoImpl
from chat_sessions.infrastructure.repositories.chat_session_repo_impl import ChatSessionRepoImpl

def get_user_repo(session = Depends(get_session)):
    return UserRepoImpl(session)

def get_token_repo(session = Depends(get_session)):
    return TokenRepoImpl(session)

def get_message_repo(session = Depends(get_session)):
    return MessageRepoImpl(session)

def get_chat_session_repo(session = Depends(get_session)):
    return ChatSessionRepoImpl(session)
