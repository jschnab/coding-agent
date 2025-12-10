import asyncio

from .gemini import GeminiAgent


def main() -> None:
    asyncio.run(start_agent())


async def start_agent():
    agent = GeminiAgent()
    await agent.start()


if __name__ == "__main__":
    main()
