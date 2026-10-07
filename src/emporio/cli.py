"""CLI mínima para testar o agente (Fase 5). Interface Streamlit na Fase 6."""

from __future__ import annotations

import argparse

from emporio.agent import responder


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat Empório da Música (CLI)")
    parser.add_argument("--verbose", action="store_true", help="Mostra tools chamadas")
    args = parser.parse_args()

    historico: list[dict[str, str]] = []
    print("Empório da Música — digite 'sair' para encerrar.\n")

    while True:
        try:
            entrada = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break
        if not entrada:
            continue
        if entrada.lower() in {"sair", "exit", "quit"}:
            print("Até logo!")
            break

        saida = responder(entrada, historico)
        print(f"\nAtendente: {saida.texto}\n")

        if args.verbose and saida.ferramentas:
            for reg in saida.ferramentas:
                print(f"  [tool] {reg.nome}({reg.argumentos})")

        historico.append({"role": "user", "content": entrada})
        historico.append({"role": "assistant", "content": saida.texto})
        if len(historico) > 20:
            historico = historico[-20:]


if __name__ == "__main__":
    main()
