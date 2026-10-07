"""Interface de chat em Streamlit para a Lúcia (Empório da Música)."""

from __future__ import annotations

import uuid

import streamlit as st

from emporio.agent import responder
from emporio.memory import (
    apagar_sessao,
    carregar_historico,
    historico_para_contexto,
    listar_sessoes,
    salvar_mensagem,
)
from emporio.prompts import NOME_ATENDENTE


def _nova_sessao() -> str:
    return uuid.uuid4().hex[:12]


def _inicializar_estado() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = _nova_sessao()
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = carregar_historico(st.session_state.session_id)


def _trocar_sessao(session_id: str) -> None:
    st.session_state.session_id = session_id
    st.session_state.mensagens = carregar_historico(session_id)


def _barra_lateral() -> None:
    with st.sidebar:
        st.header("Empório da Música")
        st.caption(f"Atendente: {NOME_ATENDENTE}")

        if st.button("➕ Nova conversa", use_container_width=True):
            _trocar_sessao(_nova_sessao())
            st.rerun()

        st.divider()
        st.subheader("Conversas anteriores")
        sessoes = listar_sessoes()
        if not sessoes:
            st.caption("Nenhuma conversa salva ainda.")
        for s in sessoes:
            rotulo = f"{s['inicio']} ({s['total']} msgs)"
            ativa = s["session_id"] == st.session_state.session_id
            prefixo = "▶ " if ativa else ""
            if st.button(f"{prefixo}{rotulo}", key=f"sess_{s['session_id']}", use_container_width=True):
                _trocar_sessao(s["session_id"])
                st.rerun()

        st.divider()
        st.session_state.mostrar_tools = st.checkbox("Mostrar ferramentas usadas", value=False)
        if st.button("🗑️ Apagar esta conversa", use_container_width=True):
            apagar_sessao(st.session_state.session_id)
            _trocar_sessao(_nova_sessao())
            st.rerun()


def main() -> None:
    st.set_page_config(page_title="Empório da Música", page_icon="🎸")
    _inicializar_estado()
    _barra_lateral()

    st.title("🎸 Empório da Música")
    st.caption(f"Converse com a {NOME_ATENDENTE}, nossa assistente virtual.")

    for msg in st.session_state.mensagens:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

    entrada = st.chat_input("Digite sua mensagem...")
    if not entrada:
        return

    session_id = st.session_state.session_id
    with st.chat_message("user"):
        st.markdown(entrada)
    st.session_state.mensagens.append({"role": "user", "content": entrada})
    salvar_mensagem(session_id, "user", entrada)

    contexto = historico_para_contexto(session_id)
    # remove a última (que acabou de entrar) para não duplicar com mensagem_usuario
    contexto_anterior = contexto[:-1] if contexto else []

    with st.chat_message("assistant"):
        with st.spinner(f"{NOME_ATENDENTE} está digitando..."):
            resposta = responder(entrada, contexto_anterior)
        st.markdown(resposta.texto)
        if st.session_state.get("mostrar_tools") and resposta.ferramentas:
            with st.expander("Ferramentas consultadas"):
                for reg in resposta.ferramentas:
                    st.write(f"**{reg.nome}** — argumentos: `{reg.argumentos}`")

    st.session_state.mensagens.append({"role": "assistant", "content": resposta.texto})
    salvar_mensagem(session_id, "assistant", resposta.texto)


if __name__ == "__main__":
    main()
