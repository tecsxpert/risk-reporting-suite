try:
    from services.rag_pipeline import load_and_store_docs
except ImportError:
    from services.rag_pipeline import load_and_store_docs


def main() -> None:
    docs = [
        "Liquidity risk arises when assets cannot be traded quickly enough, leading to potential losses.",
        "Operational risk includes system failures, cyber attacks, and human error that disrupt trading.",
        "Credit risk occurs when borrowers default on repayment obligations, weakening financial stability.",
    ]

    result = load_and_store_docs(docs)
    print(result)


if __name__ == "__main__":
    main()
