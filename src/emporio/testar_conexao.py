"""Script mínimo para validar chave e SDK da OpenAI (Fase 0)."""

import sys

from emporio.llm import ErroSaldoInsuficiente, gerar_texto


def main() -> None:
    try:
        resposta = gerar_texto(
            "Responda em uma palavra: ok",
        )
    except ErroSaldoInsuficiente as erro:
        print(f"Falha: {erro}", file=sys.stderr)
        raise SystemExit(1) from erro
    print(f"OpenAI respondeu: {resposta}")


if __name__ == "__main__":
    main()
