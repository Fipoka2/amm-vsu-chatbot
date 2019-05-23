from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill


def reload():
    faq = SimilarityMatchingSkill(data_path='dataset_vsu_qa.csv',
                                  x_col_name='Question',
                                  y_col_name='Answer',
                                  save_load_path='./model',
                                  config_type='tfidf_autofaq',
                                  edit_dict={},
                                  train=True)
