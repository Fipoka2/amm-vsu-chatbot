from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector

faq = SimilarityMatchingSkill(data_path='dataset_vsu_qa.csv',
                              x_col_name='Question',
                              y_col_name='Answer',
                              save_load_path='./model',
                              config_type='tfidf_autofaq',
                              edit_dict={},
                              train=False)

hello = PatternMatchingSkill(responses=['Привет', 'Приветствую'],
                             patterns=['Привет', 'Здравствуйте'])
bye = PatternMatchingSkill(responses=['Пока', 'Всего доброго'], patterns=['Пока', 'До свидания'])
fallback = PatternMatchingSkill(responses=['Пожалуйста перефразируйте'], default_confidence=0.3)

agent = DefaultAgent([hello, bye, faq, fallback], skills_selector=HighestConfidenceSelector())
print(agent(['Привет'], [1])[0])

idx = 0
while True:
    question = input("your question:")
    if question is 'exit':
        break
    print(agent([question], [0]))
