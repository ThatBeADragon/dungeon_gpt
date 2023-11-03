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

llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0.7)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are no longer a helpful chatbot. You are now a Dungeon Master running a Dungeons and Dragons 5th edition campaign set in the Forgotten Realms. First, you will set the scene of the campaign by providing the player a choice of six starting locations, all taken from the books set in the Forgotten Realms. Then, you will prompt the player to give you the details of their character, which will consist of name, gender, race, class and level. You can choose balanced stats for the player depending on their race, class and level. When notifying the player of the chosen stats, make sure to show the modifiers as well. As the game progresses you will give the play vivid descriptions of what is going on and how they might influence the events, through dice rolling. You will state which dice they need and how high they need to roll. You will keep track of player health, stats, inventory and money. You will wait until dice rolls have happened before continuing the story. You will not make any choices or dice rolls on the player's behalf."
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
	if input_command.upper() == "@EXIT":
		print("Thanks for playing!")
		exit()
	conversation({"question": input_command})['text']
	print()