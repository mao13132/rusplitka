from src._main import main

if __name__ == '__main__':
    step1_get_brand = False  # Шаг с парсингом брендов

    step2_pars_brand_collections = True  # Шаг с парсингом коллекций в бренде

    step3_pars_in_collection_product = True  # Шаг с парсингом внутренностей коллекций и забором товаров из них

    step4_pars_product = True  # Шаг с парсингом внутренностей товаров

    main(step1_get_brand, step2_pars_brand_collections, step3_pars_in_collection_product, step4_pars_product)
