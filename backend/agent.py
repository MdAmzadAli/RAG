from autogen import AssistantAgent, UserProxyAgent, register_function, config_list_from_json
from embeddings import embedding_model
from vector_store import query_qdrant

config=config_list_from_json("config.json")

def query_with_agent_and_return(question, user_id, file_id):
    final_answer = {"content": ""}
    
    def search_user_file(query: str) -> str:
        vector = embedding_model.embed_query(query)
        return query_qdrant(vector, user_id, file_id)

    def store_answer(content: str) -> str:
        final_answer["content"] = content
        return "Answer stored successfully."
    
    assistant = AssistantAgent(
        name="DocumentAgent",
        system_message=(
            "You are a document assistant. Use `search_user_file(question)` to find relevant content "
            "and answer based only on it. Once you have the final answer, call `store_answer(content)` "
            "to save it and end the conversation with the phrase 'Final Answer'."
        ),
        llm_config={"config_list": config},
    )

    # Create user agent
    user = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        is_termination_msg=lambda x: "Final Answer" in x.get("content", ""),
        code_execution_config=False,
    )

    # Register tools with agents
    register_function(search_user_file, caller=assistant, executor=user)
    register_function(store_answer, caller=assistant, executor=user)

    # Start the conversation
    user.initiate_chat(assistant, message=question)

    return final_answer["content"]
