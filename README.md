# wiki_run
Алгоритм, который начиная с заданной страницы на Википедии с помощью word2vec модели ищет целевую страницу(сравнивая векторы всех гиперссылок с целью). DFS/BFS не используется намеренно ;) <br />
<i>Пример: 'человек' -> 'млекопитающие' -> 'лучепёрые рыбы' -> 'новопёрые рыбы' -> 'рыбы' -> 'лопастепёрые рыбы' -> 'костные рыбы' -> 'хрящевые рыбы' -> 'моллюски' ->  'виноградная улитка' ->'гриб'.</i> <br />
Как видно, тут была масса возможностей сократить путь, но моделька, не обладающая какими-либо знаниями о нашем мире и способностями к мышлению, просто искала связи между тем, что видела, и тем, что ей было надо найти<br />
## Как попробовать
1. Установка всех модулей для python3.6+: <br />
<code>pip install -r requirements.txt</code> <br />
2. Запустите <code>Vectorizer.py</code> для установки word2vec модели. 
3. В <code>main.py</code> начальная страница указывается в переменной <code>url</code>, цель(название страницы) - в <code>target</code>. Запуск проги - <code>start.bat</code>
## Эффективность
Тут либо эффективность, либо скорость - если избавиться от ограничения на количество обрабатываемых гиперссылок(<code>MAX_LINKS</code>), то результативность будет практически стопроцентная, однако скорость работы станет очень низкой(на некоторых страницах гиперссылок очень много). По понятным причинам, с слишком маленьким <code>MAX_LINKS</code> результативность будет маленькой - шанс наткнуться на нужную гиперссылку невелик вне зависимости от порядка обработки. Я указал <code>MAX_LINKS=300</code>, посчитав это балансом эффективности и скорости.
## Кое-какие тонкости и косяки
Из-за тонкостей структуры самой Википедии алгоритм иногда путается и пытается пойти в более позднюю/раннюю версию той же страницы с отличающейся ссылкой - в таких случаях мы возвращаемся на 1 шаг и добавляем "плохую" ссылку в блэклист. Если минимальное косинусное расстояние среди всех векторизованных ссылок(самое "похожее" на цель) > 1 или подходящих ссылок вообще обнаружено не было, мы так же возвращаемся на 1 шаг. Если по какой-то причине нам не удается перейти по ссылке(например, мы каким-то образом, возможно, из-за бага, возвращаемся на одну и ту же страницу много раз и нам запрещают доступ), то возвращаемся в самое начало и идем по совершенно другому пути. Это откровенный косяк, решенный костылем, но я верю, что такое легко пофиксить.
