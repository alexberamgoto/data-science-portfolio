
def afficher_deces(data):
    """
    visualisation des deces du fichier csv
    :param data:
    :return:
    """








    #test*
    if __name__ == '__main__':
        model= Modele("big.csv")
        data= model.data
        serie=controleur.select_data_deces(data,
                                           departement='75',
                                           de=datetime(2020,3,19),
                                           a=datime(2023,1,26))
        Vue.afficher_deces(serie)