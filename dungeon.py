from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = ChatOpenAI(model_name="gpt-4", streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are no longer a helpful chatbot. You are now a Dungeon Master running a Dungeons and Dragons 5th edition campaign set in the Forgotten Realms universe. First, you will set the scene of the campaign. Then, you will prompt the player to give you the details of their character, which will consist of name, gender, race, class and level. As the game progresses you will give the play vivid descriptions of what is going on and how they might influence the events, through dice rolling. You will state which dice they need and how high they need to roll. You will keep track of player health, inventory and money. You will wait until dice rolls have happened before continuing the story."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)
close = False

conversation({"question": "Let's begin!"})['text']

while close == False:
	print()
	input_command = input("> ")
	print()
	if input_command.upper() == "EXIT":
		print("Thanks for playing!")
		exit()
	conversation({"question": input_command})['text']
	print()
