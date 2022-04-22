def prefilter_items(purchases_data, take_n_popular=None, n_rows=None):
    popularity = purchases_data.groupby('item_id')['user_id'].nunique().reset_index()
    popularity['share_unique_users'] = popularity['user_id'] / purchases_data[
        'user_id'].nunique()
    popularity.drop('user_id', axis=1, inplace=True)
    # Уберем самые популярные товары (их и так купят)
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    res = purchases_data[~purchases_data['item_id'].isin(top_popular)]

    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    res = res[~res['item_id'].isin(top_notpopular)]

    purchase_weeks = purchases_data.groupby('item_id')['week_no'].max().reset_index()
    purchase_weeks.columns = ['item_id', 'last_week']
    # Уберем товары, которые не продавались за последние 12 месяцев
    last_12_month_unpurchasable = purchase_weeks[purchase_weeks['last_week'] <= (max(purchases_data['week_no']) - 48)]
    res = res[~res['item_id'].isin(last_12_month_unpurchasable['item_id'])]

    # Из текущей выборки еще раз отбираем популярные для среза take_n_popular
    second_popularity = purchases_data.groupby('item_id')['user_id'].nunique().reset_index()
    second_popularity['share_unique_users'] = second_popularity['user_id'] / purchases_data[
        'user_id'].nunique()
    second_popularity.drop('user_id', axis=1, inplace=True)
    low_popularity = second_popularity.sort_values('share_unique_users')[:-take_n_popular]
    #Отрезаем из данных все low_popularity
    res = res[~res['item_id'].isin(low_popularity['item_id'])]

    # Уберем не интересные для рекоммендаций категории (department) В текущих датасетах нет смысла убирать колонку.
    # Мы же должны фильтровать item_id для удаления, а удалив колонку в датасете, мы ничего не отфильтруем.
    # Либо надо брать подмножество department конкретное тогда, как мне кажется

    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.
    # Стоимости товаров у нас нет в данных, только объем продаж

    # Уберем слишком дорогие товарыs

    # ...

    return res[:n_rows]
