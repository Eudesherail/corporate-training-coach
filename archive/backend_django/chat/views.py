import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .agents.agent_factory import AgentFactory


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def message(request):
    data = json.loads(request.body.decode('utf-8'))
    user = request.user

    # Erstellen Sie eine Instanz des Agents
    agent_instance = AgentFactory.create_agent(user)

    # Führen Sie den Agent aus, um eine Antwort zu erhalten
    response = agent_instance.execute(data.get('message'))
        
    if not response:
        return JsonResponse({"message": "Es ist tut mir leid, ich hab dich nicht verstanden! 😧 Könntest du das vielleicht nochmal anders formulieren?"}, status=500)

    final_answer = parse_final_answer(response)
    return JsonResponse({"message": response})
    
def parse_final_answer(agent_output):
    start_token = "Final Answer:"
    end_token = "\n"  # Assuming each section is separated by new lines

    # Find the start and end of the "Final Answer" section
    start_index = agent_output.find(start_token)
    end_index = agent_output.find(end_token, start_index)

    if start_index != -1:
        final_answer = agent_output[start_index + len(start_token):end_index].strip()
        return final_answer
    else:
        return agent_output
