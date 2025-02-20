@pytest.mark.asyncio
async def test_bot_initialization():
    bot = SolanaWealthyBot()
    assert bot.token_configs == {}