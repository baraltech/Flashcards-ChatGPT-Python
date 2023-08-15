import openai
import pygame
import sys

API_KEY = open('key.txt', 'r').read()
openai.api_key = API_KEY

text = str(open('source_text.txt', 'r').read())

flashcards = {}

create_or_load = input("Would you like to create a new set of flashcards (1) or load a previous set (2)?: ")

if create_or_load.strip() == '1':    
    while True:
        try:
            flashcard_count = int(input("Enter the number of flashcards you'd like to create: "))
            break
        except:
            print("Please enter a valid integer.")
            continue
    
    name = input("Please enter the name of the text file to store the flashcards: ")

    prompt = "Create " + str(flashcard_count) + """ flashcards
    that fully encapsulate all the concepts in the following piece of text. The flashcards should be
    formatted with "Question: " followed by the question and "Answer: " followed by the answer.
    """ + f"\n{text}"

    # print(prompt)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    chatgpt_response = response['choices'][0]['message']['content']

    qa_pairs = chatgpt_response.strip().split('\n\n')

    parsed_data = {}
    
    for qa_pair in qa_pairs:
        question, answer = qa_pair.split('\n')
        question = question.replace("Question: ", "")
        answer = answer.replace("Answer: ", "")
        parsed_data[question] = answer

    flashcards = parsed_data

    with open(f'{name}.txt', 'w') as flashcards_file:
        flashcards_file.write(str(parsed_data))
else:
    while True:
        try:
            load_name = input("Please enter the name of the text file to load the flashcards: ")
            flashcards = eval(open(f'{load_name}.txt', 'r').read())
            break
        except:
            print("Invalid name!")
            continue
    

pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Quiz App")

BG_COLOUR = "#0a092d"
FLASHCARD_COLOUR = "#2e3856"
FLIPPED_COLOUR = "#595e6d"
FONT = pygame.font.SysFont("Arial", 30)

SCREEN.fill(BG_COLOUR)

current_question = ""
current_answer = ""

card_turned = False

index = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                card_turned = not card_turned
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and index < len(flashcards) - 1:
                index += 1
                card_turned = False
            elif pygame.key.get_pressed()[pygame.K_LEFT] and index > 0:
                index -= 1
                card_turned = False
    
    current_question = list(flashcards)[index]
    current_answer = list(flashcards.values())[index]
    current_question_object = FONT.render(current_question, True, "white", wraplength=450)
    current_question_rect = current_question_object.get_rect(center=(400, 400))
    current_answer_object = FONT.render(current_answer, True, "white", wraplength=450)
    current_answer_rect = current_answer_object.get_rect(center=(400, 400))
    current_index_object = FONT.render(f"{index+1}/{len(flashcards)}", True, "white")
    current_index_rect = current_index_object.get_rect(center=(400, 600))
    
    if not card_turned:
        SCREEN.fill(BG_COLOUR)
        pygame.draw.rect(SCREEN, FLASHCARD_COLOUR, (150, 250, 500, 300))
        SCREEN.blit(current_question_object, current_question_rect)
    else:
        SCREEN.fill(BG_COLOUR)
        pygame.draw.rect(SCREEN, FLIPPED_COLOUR, (150, 250, 500, 300))
        SCREEN.blit(current_answer_object, current_answer_rect)
    
    SCREEN.blit(current_index_object, current_index_rect)
    
    pygame.display.update()