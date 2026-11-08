# Builds the static GalA-Consult site into site/  (run: python3 build/build.py)
import json, math, os, re, html, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import logos

SITE = os.path.join(ROOT, 'site')
MAP = json.load(open(os.path.join(HERE, 'map.json')))
DOMAIN = 'https://galaconsult.kz'
E = html.escape

# ---------------- icons ----------------
def ic(body, sw=1.7):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
I = {
    'arrow': ic('<path d="M4 12h15M13 6l6 6-6 6"/>'),
    'left': ic('<path d="M20 12H5M11 6l-6 6 6 6"/>'),
    'ext': ic('<path d="M7 17 17 7M9 7h8v8"/>'),
    'clip': ic('<path d="M20.5 11.5 12 20a5.5 5.5 0 0 1-7.8-7.8l8.6-8.6a3.7 3.7 0 0 1 5.2 5.2l-8.6 8.6a1.8 1.8 0 0 1-2.6-2.6l7.9-7.9"/>'),
    'copy': ic('<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/>'),
    'pin': ic('<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    'mail': ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>'),
    'x': ic('<path d="M6 6l12 12M18 6 6 18"/>'),
    'up': ic('<path d="M12 19V5M6 11l6-6 6 6"/>'),
    'law': ic('<path d="M12 4v16M7.5 20h9M5 7.5h14M8 4.8 12 4l4 .8"/><path d="M5 7.5 2.5 13a2.6 2.6 0 0 0 5 0L5 7.5zM19 7.5 16.5 13a2.6 2.6 0 0 0 5 0L19 7.5z"/>'),
    'market': ic('<path d="M3 21h18M5 21V10.5L12 6l7 4.5V21"/><path d="M9.5 21v-5.5h5V21M12 6V2.8l3.5 1.4L12 5.6"/>'),
    'globe': ic('<circle cx="12" cy="12" r="8.6"/><path d="M3.4 12h17.2M12 3.4c2.4 2.5 3.6 5.4 3.6 8.6s-1.2 6.1-3.6 8.6M12 3.4C9.6 5.9 8.4 8.8 8.4 12s1.2 6.1 3.6 8.6"/>'),
    'talk': ic('<path d="M3.5 5.5h10a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H8.5L5 17.3v-2.8H3.5a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2z"/><path d="M18.5 9.5h.5a2 2 0 0 1 2 2v4.5a2 2 0 0 1-2 2h-.5v2.6l-3-2.6h-3.5"/>'),
    'book': ic('<path d="M5 4.5h10.5A2.5 2.5 0 0 1 18 7v13H7a2 2 0 0 1-2-2z"/><path d="M5 18a2 2 0 0 1 2-2h11M9 8.5h5"/>'),
    'flow': ic('<rect x="3" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="14.5" y="13.5" width="6.5" height="6.5" rx="1.5"/><path d="M9.5 7.2h3.5a2.5 2.5 0 0 1 2.5 2.5v3.8"/>'),
    'people': ic('<circle cx="8.5" cy="8" r="3"/><circle cx="16.8" cy="9.2" r="2.4"/><path d="M3 19.5c.6-3.3 2.9-5.2 5.5-5.2s4.9 1.9 5.5 5.2M14.2 14.4c.8-.3 1.7-.4 2.6-.4 2.2 0 3.9 1.5 4.4 4.5"/>'),
}
DOCFILE = ('<svg viewBox="0 0 40 48" aria-hidden="true"><path d="M7 1.5h19.5L37.5 12.5V44a2.5 2.5 0 0 1-2.5 2.5H7A2.5 2.5 0 0 1 4.5 44V4A2.5 2.5 0 0 1 7 1.5z" fill="#fff" stroke="#AEBBD1"/>'
           '<path d="M26.5 1.5V10a2.5 2.5 0 0 0 2.5 2.5h8.5" fill="#E9EEF7" stroke="#AEBBD1"/><path d="M10.5 18h17M10.5 23h17M10.5 28h11" stroke="#CAD4E4" stroke-width="1.6" stroke-linecap="round"/></svg>')

# ---------------- projects ----------------
P = [
 dict(slug='bavaria-water-2026', type='Деловая поездка', flag='de', place='Бавария, Германия', dates='29 июня - 4 июля 2026', year=2026,
      short='Водное хозяйство, водообеспечение и управление сточными водами',
      title='Деловая поездка в Баварию для организаций и предприятий Казахстана из отрасли «Водное хозяйство. Водообеспечение. Управление сточными водами»',
      theme=None, topic='Водное хозяйство, водообеспечение, сточные воды',
      program='Bayern - Fit for Partnership; Bayern International, em&amp;s GmbH',
      body=[
        ('p', 'ТОО «ГалА-Консалт» совместно с немецкой компанией em&amp;s GmbH организует деловую поездку казахстанских специалистов водного хозяйства в Баварию. Поездка проходит в рамках программы «Bayern - Fit for Partnership», которую инициирует и финансирует Министерство экономики Баварии, а курирует Bayern International.'),
        ('h3', 'Темы программы'),
        ('ul', ['Планирование, строительство и модернизация очистных сооружений, в том числе малых', 'Сооружения для обработки осадка', 'Современные технологии водоподготовки', 'Реконструкция и расширение канализационных сетей', 'Энергоэффективная эксплуатация очистных сооружений', 'Повторное использование очищенной воды']),
        ('h3', 'Что входит в программу'),
        ('ul', ['Посещение баварских компаний, демонстрации продукции и оборудования, презентации', 'Посещение референтных объектов в Баварии', 'Презентация и день открытых дверей 30 июня 2026 года в Баварском земельном ведомстве по охране окружающей среды в Хофе', 'Перевод на мероприятиях программы']),
        ('h3', 'Участники'),
        ('p', 'В составе делегации - около 15 руководителей водоканалов, инжиниринговых и строительных компаний, поставщиков решений, а также импортеры, монтажные организации, представители городских структур, принимающих инвестиционные решения, и представитель министерства.'),
        ('callout', 'Программа поездки и анкета участника - в приложениях к письму.'),
      ],
      docs=[('Анкета участника', 'docx', None, 'Заполнить и прислать на gaco@galaconsult.kz'), ('Программа поездки', 'pdf', None, 'Маршрут, компании и объекты по дням')]),
 dict(slug='ifat-eurasia-2025', type='Выставка', flag='tr', place='Стамбул, Турция', dates='15-17 мая 2025', year=2025,
      short='IFAT Eurasia 2025: водоснабжение, очистка сточных вод и отходы',
      title='Поездка в Стамбул на выставку «IFAT Eurasia» с 15 по 17 мая 2025 года',
      theme='Технологии водоснабжения и очистки сточных вод, управление, переработка, утилизация отходов, транспортные средства для очистки городской среды, предотвращение загрязнения, безопасность труда.',
      topic='Экологические технологии, водоснабжение, отходы', venue='Tüyap Fair and Congress Center',
      program='По поручению Messe München', deadline='15 апреля 2025',
      body=[
        ('salute', 'Уважаемые дамы и господа, уважаемые предприниматели,'),
        ('p', 'По поручению выставочной организации Баварии «Messe München» ТОО «ГалА-Консалт» организует посещение казахстанской делегацией выставки «IFAT Eurasia», которая состоится с 15 по 17 мая 2025 года в Tüyap Fair and Congress Center в Стамбуле.'),
        ('p', '«Messe München» является организатором крупнейших международных выставок, в том числе выставки IFAT, как в Германии, так и в разных странах мира. IFAT Eurasia - ведущий технологический хаб между Азией и Европой, охватывающий рынки Юго-Восточной Европы, Северной Африки и Ближнего Востока.'),
        ('p', 'В очередной раз на выставке будет представлен широкий спектр продуктов и услуг, предназначенных для решения постоянно растущих экологических проблем, с которыми сталкивается сегодня мир. Первоклассная программа поддержки включает интерактивные групповые дискуссии и семинары.'),
        ('h3', 'Для участников делегации'),
        ('ul', ['Групповая фотография', 'Бесплатный бейдж на время выставки, подготовленный заранее, чтобы не ждать у стоек регистрации', 'Организованные встречи с выбранными экспонентами в соответствии с пожеланиями группы']),
        ('p', 'Надеемся на участие в делегации предпринимателей и специалистов соответствующих отраслей, организаций. В случае возникновения вопросов мы всегда в Вашем распоряжении: <a href="mailto:gaco@galaconsult.kz">gaco@galaconsult.kz</a>, <a href="mailto:info@galaconsult.kz">info@galaconsult.kz</a>, тел. <span class="nw">+7 701 550-99-00</span>.'),
        ('callout', 'В случае интереса к посещению выставки просим заполнить анкету (приложение 1) и прислать ее нам не позднее <b>15 апреля 2025 г.</b> по адресам: gaco@galaconsult.kz, info@galaconsult.kz.'),
      ],
      sign=True,
      docs=[('Анкета участника', 'docx', None, 'Прислать до 15 апреля 2025'), ('Информационное письмо Messe München', 'doc', 'https://docs.google.com/document/d/1VPnnxDELblZDQBxUPQEtDhqeqQLTDbPx/edit', 'Описание проекта и программы визита')]),
 dict(slug='bavaria-medical-2024', type='Деловая поездка', flag='de', place='Бавария, Германия', dates='1-6 июля 2024', year=2024,
      short='Медицинская отрасль: торговля, менеджмент, сервис',
      title='Поездка в Баварию для организаций и предприятий, обслуживающих медицинскую отрасль (торговля, менеджмент, сервис)',
      theme=None, topic='Медицинская отрасль', program='Bayern - Fit for Partnership',
      body=[
        ('p', 'Деловая поездка в Баварию для казахстанских организаций и предприятий, обслуживающих медицинскую отрасль: торговля, менеджмент, сервис. Поездка проходит в рамках баварской программы «Bayern - Fit for Partnership» по направлению «Медицинская техника для Казахстана».'),
        ('callout', 'Программа поездки и анкета участника - в приложениях к письму.'),
      ],
      docs=[('Анкета участника', 'docx', None, 'Заполнить и прислать на gaco@galaconsult.kz'), ('Программа поездки', 'pdf', None, 'Маршрут, компании и объекты по дням')]),
 dict(slug='bavaria-packaging-2023', type='Информационная поездка', flag='de', place='Бавария, Германия', dates='19-23 июня 2023', year=2023,
      short='Упаковка и бумажная промышленность',
      title='Информационная поездка в Баварию для предприятий отрасли «Упаковка и бумажная промышленность» Республики Казахстан',
      theme=None, topic='Упаковка, бумажная промышленность', program='Bayern - Fit for Partnership',
      body=[
        ('p', 'Информационная поездка в Баварию для казахстанских организаций и предприятий отрасли упаковки и бумажной промышленности. Поездка проходит в рамках баварской программы «Bayern - Fit for Partnership» по направлению «Машиностроение: бумажная и упаковочная промышленность для Казахстана».'),
        ('callout', 'Программа поездки и анкета участника - в приложениях к письму.'),
      ],
      docs=[('Анкета участника', 'docx', None, 'Заполнить и прислать на gaco@galaconsult.kz'), ('Программа поездки', 'pdf', None, 'Маршрут, компании и объекты по дням')]),
 dict(slug='ifat-eurasia-2023', type='Выставка', flag='tr', place='Стамбул, Турция', dates='27-29 апреля 2023', year=2023,
      short='IFAT Eurasia 2023: экологические технологии и водные ресурсы',
      title='Визит казахстанской делегации предпринимателей на выставку «IFAT Eurasia»',
      theme='Экологические технологии, управление водными ресурсами.', topic='Экологические технологии, водные ресурсы', program=None,
      body=[
        ('p', 'Визит делегации казахстанских предпринимателей на международную выставку экологических технологий «IFAT Eurasia» в Стамбуле, 27-29 апреля 2023 года.'),
        ('callout', 'Программа визита и анкета участника - в приложениях к письму.'),
      ],
      docs=[('Анкета участника', 'docx', None, 'Заполнить и прислать на gaco@galaconsult.kz'), ('Программа визита', 'pdf', None, 'Выставка, встречи и экскурсии')]),
 dict(slug='saxony-machinery-2023', type='Выставка', flag='de', place='Саксония, Германия', dates='7-10 марта 2023', year=2023,
      short='Машиностроение',
      title='Визит делегации казахстанских предприятий на выставку в Саксонию',
      theme='Машиностроение.', topic='Машиностроение', program=None,
      body=[
        ('p', 'Визит делегации казахстанских предприятий на выставку в Саксонию, 7-10 марта 2023 года. Тема: машиностроение.'),
        ('callout', 'Программа визита и анкета участника - в приложениях к письму.'),
      ],
      docs=[('Анкета участника', 'docx', None, 'Заполнить и прислать на gaco@galaconsult.kz'), ('Программа визита', 'pdf', None, 'Выставка, встречи и экскурсии')]),
]
OLD_SLUGS = {'july2024': 'bavaria-medical-2024'}

WC_D = 'm718 119c-2 0-4-1-6-1c-1 0-2 0-3 0c0 0-1 0-3-1c0 0-2-1-3-1c-1 0-1 0-2 0c-1 0-2-1-3-1c-3-1-9-3-10-4c0 0-1-1-2-1c0 0-1 0-1 0c-1 0-2-1-3-2c-2-1-3-2-4-2c-1-1-2-2-3-2c-1-1-1-2-2-2c-1-1-5-4-7-6c0 0-1-2-2-2c0 0-1-2-2-3c-1-1-4-7-4-7c0 0 0-1-1-2c0 0-1-1-1-2c0 0 0-1 0-1c0-1-1-2-1-3c0 0-1-2-1-3c0-1 0-2-1-3c0-1 0-3 0-4c-1-3-1-10 0-12c0-2 0-4 1-4c0-2 0-3 0-4c0 0 1-1 1-2c0 0 3-8 5-12c4-6 8-10 14-15c1-1 2-1 2-1c1-1 2-2 3-2c1 0 1-1 2-2c1 0 7-3 9-4c0 0 0 0 1 0c1-1 2-1 4-2c1 0 2-1 3-1c2-1 3-1 4-1c0 0 1 0 1 0c0-1 1-1 3-1c2-1 4-1 5-1c3-1 5-1 7-1c0 0 3 0 5-1c5 0 14 0 21 1c4 0 7 1 7 1c3 0 5 1 7 1c1 0 2 1 3 1c1 0 2 0 3 0c0 1 2 1 3 2c1 0 2 0 3 0c0 1 1 1 1 1c1 0 10 4 11 5c1 0 2 1 3 2c3 1 4 2 4 3c0 0 0 1 0 1c-1 1-2 3-3 4c0 1-1 2-1 2c-2 3-2 3-4 2c-1-1-2-2-4-2c0-1-1-1-1-2c0 0-1 0-1 0c0 0-1-1-3-2c-2 0-4-1-4-1c0 0-1-1-1-1c-1 0-2 0-2-1c-1 0-2 0-2 0c-1-1-2-1-3-1c0 0-1 0-2-1c-1 0-2-1-4-1c-2 0-3 0-3 0c-1 0-3-1-5-1c-3 0-6-1-7-1c-3 0-13 0-18 0c-2 0-4 1-4 1c-1 0-7 1-10 1c-3 1-6 2-8 4c-1 0-3 0-4 1c-1 1-6 3-8 4c-2 1-3 3-5 5c-5 4-10 10-11 14c0 0-1 2-1 3c-1 1-2 3-2 5c0 1 0 3-1 4c0 2 0 9 0 13c1 4 1 6 2 7c0 0 0 1 1 2c0 1 3 7 3 8c1 0 1 0 1 0c2 2 6 7 7 8c4 3 7 5 8 6c1 0 1 1 2 1c0 1 1 1 1 1c1 0 2 0 2 1c1 0 2 1 2 1c0 0 1 0 2 0c1 0 2 1 2 1c1 0 2 1 2 1c1 0 2 0 3 0c1 1 2 1 3 1c0 1 2 1 4 1c1 0 2 1 3 1c2 1 11 1 19 1c5 0 9 0 10-1c2 0 6-1 7-1c1 0 3 0 3-1c0 0 2 0 2 0c2-1 5-1 8-2c4-2 5-2 8-3c1-1 3-2 3-2c1-1 1-1 2-2c1 0 2-1 3-2c2 0 2-1 3-1c0 0 1 1 3 4c0 1 1 3 2 3c0 1 1 2 1 2c0 1 0 1-1 2c-1 0-5 3-7 4c-1 0-1 0-1 0c-2 1-7 4-8 4c0 0-1 0-2 0c0 1-1 1-2 2c0 0-1 0-2 0c-2 1-8 2-10 2c0 0-2 1-2 1c-1 1-2 1-3 1c-1 0-5 0-9 1c-3 0-19 0-24 0zm-651-2c0 0-1 0-2 0c-2 0-2 0-3-1c0 0-1 0-1-1c0 0-1-2-3-5c-1-2-2-5-3-6c-1-2-2-5-3-6c0 0 0 0 0-1c0-1-2-2-2-4c-3-3-4-7-6-9c0-1-1-2-2-3c0-1 0-2 0-3c-1 0-2-3-4-6c-4-6-6-10-7-12c-1-2-1-2-1-3c0 0-1-1-2-3c-2-3-4-8-5-9c0-1-1-1-1-2c0-1-1-1-2-3c0 0-1-2-1-2c0 0-1-1-1-1c0-1 0-1 0-2c-1 0-1-1-2-1c0-1 0-2 0-2c0 0 0-1-1-1c0 0-1-2-1-3c-1-2-2-4-3-4c0-2-1-3-1-4c-2-2-3-5-5-7c0-1-1-3-2-4c0-1-1-3-2-4c-1-1-1-2 0-2c1-1 4-1 7-1l7 0l1 1c0 1 1 1 1 2c0 1 1 1 1 2c0 0 0 1 1 1c0 1 0 2 0 2c1 0 1 1 1 2c0 0 1 1 2 2c0 2 3 6 4 8c0 0 1 1 1 2c1 1 2 2 2 4c1 0 1 2 2 2c0 1 1 2 1 2c0 1 0 2 1 2c0 0 1 2 1 3c3 5 4 8 5 9c0 0 1 1 3 4c0 2 2 5 4 8c1 2 3 6 4 8c1 2 2 4 2 4c1 1 1 2 1 2c0 0 0 0 1 0c0 0 0 2 1 4c1 1 2 2 2 2c0 1 1 2 2 4c1 3 2 4 5 9c0 1 1 2 2 3c0 2 1 3 1 3c0 0 0 1 1 1c0 1 1 2 1 3c1 1 1 1 1 1c1 0 1 0 2-2c1-3 3-5 3-6c0 0 1-2 3-5c1-2 2-4 2-5c1 0 2-2 2-4c1-1 2-2 2-2c0-1 1-2 1-2c1-1 1-2 3-5c0-1 1-3 2-3c0-1 1-2 2-4c2-4 4-6 4-7c0 0 0 0 0-1c0 0 1-2 2-3c0-1 1-3 2-4c0-1 1-1 1-2c3-5 5-9 5-10c1-1 1-1 1-1c0 0 1-1 1-2c1-2 2-4 3-5c1-1 1-3 2-3c0 0 0-1 1-2c0-1 2-3 2-4c1-2 2-3 2-4c0 0 0 0 1-1c0-1 1-1 1-1c0 0 0-2 1-2c0-1 1-2 1-3c0-1 1-1 1-1c1-1 1-2 2-3c1-2 1-2 4-2c1-1 2-1 2 0c1 0 1 1 2 3c1 2 2 4 3 4c0 1 1 4 2 6c2 2 3 4 4 5c0 1 1 2 1 3c2 3 6 11 8 14c0 0 1 2 1 2c1 2 4 6 4 8c2 2 4 6 4 8c4 5 4 6 7 12c1 0 2 2 2 4c1 1 2 3 3 4c0 0 1 2 2 4c1 1 2 3 2 3c0 0 0 1 0 1c1 2 4 7 4 8c0 0 0 0 1 0c0 1 1 2 1 3c1 1 1 2 2 3c0 0 0 1 0 1c0 0 1 1 1 1c1 2 2 2 3 0c0-1 2-2 2-3c0-1 1-1 1-2c0 0 1-1 1-2c2-3 5-9 8-13c0-2 1-4 2-4c0-2 1-4 2-5c1-1 2-3 2-3c0 0 1-2 2-3c4-7 4-8 7-13c1-2 2-4 3-5c0-1 1-3 2-4c1-2 3-6 5-10c1-2 2-4 3-6c1-1 2-3 2-4c0 0 1-1 1-1c1-1 1-2 4-7c1-2 2-5 3-5c0-1 1-2 1-3c1-3 2-4 3-4c1-1 14-1 15 0c0 0 0 0-1 1c0 2-3 6-3 7c-1 1-2 3-3 5c-1 1-2 4-3 5c-1 2-2 4-4 8c0 0-1 1-2 3c-2 4-3 5-3 6c0 1-1 2-2 3c-1 3-2 4-3 5c0 1-1 2-1 2c0 1-3 6-6 12c-1 0-1 2-2 3c-1 1-1 2-3 6c-1 1-2 3-2 3c-1 0-1 1-1 1c0 0-1 2-2 4c-1 2-2 5-3 6c-2 3-6 10-7 12c0 1-2 3-2 4c-3 5-6 11-7 13c0 0-1 2-1 2c0 0 0 1 0 1c-1 1-1 1-2 1c0 1 0 1-7 1c-4 0-8-1-8-1c-1 0-1 0-1-1c-1-1-1-2-2-3c0 0-1-2-1-2c0 0 0-1-1-1c0-1-1-3-2-5c-2-3-2-4-3-5c0-1-1-1-1-2c0-1-1-2-2-2c-1-3-2-4-2-5c0 0-2-2-3-4c-1-2-2-4-2-4c0 0 0-1-1-2c0 0 0-1-1-2c0 0 0 0 0-1c-1-1-1-1-2-3c0 0-1-2-1-2c0 0-1-2-1-2c0 0-1-1-1-2c-1-1-2-3-3-4c-1-2-1-3-1-3c0 0 0-1-1-1c0 0-1-2-2-4c-3-4-4-7-5-9c0-1-1-1-1-2c0-1-1-1-1-1c0 0 0-2-1-3c-2-4-5-8-6-10c-1-1-1-2-1-3c-1-1-2-1-2 0c0 0-1 0-1 1c-1 2-2 4-4 7c-1 0-2 3-3 5c-1 2-2 4-2 5c-1 0-1 1-2 2c-2 3-4 7-5 9c0 1-1 2-1 3c-1 0-1 1-2 2c0 1-2 4-4 7c0 1-2 3-2 5c-1 2-2 4-2 4c-1 1-2 2-2 3c0 1-1 1-1 2c-1 1-1 2-2 3c-1 3-4 8-5 10c0 1-1 2-2 2c0 0 0 2 0 2c-1 1-2 4-3 5c-1 2-3 4-3 4c0 0-1 2-2 3c0 2-2 4-2 4c0 0-1 1-3 1c-2 0-4 0-5 0c-2 0-3 0-3 0zm409-1l0 0l-1-56c0-46 0-57 1-57c0 0 81-1 83 0c0 0 1 0 2 0c1 0 3 1 4 1c1 0 2 0 3 0c1 0 2 0 3 1c0 0 1 0 3 1c4 1 7 2 9 4c0 0 1 0 1 0c1 0 6 5 8 8c1 1 2 4 3 6c0 0 0 2 0 2c1 2 1 3 1 6c0 4 0 4 0 6c-1 1-1 2-1 2c0 1-3 6-4 7c-1 2-4 4-6 5c-1 1-1 2-2 2c-1 0-3 2-5 2c-1 1-2 2 0 2c0 0 2 1 3 1c1 1 2 1 3 1c0 1 0 1 0 1c0 0 1 0 2 1c0 0 2 1 2 2c3 1 6 4 7 5c3 3 4 6 4 8c1 1 1 2 1 3c0 1 0 2 0 6c0 4 0 4 0 7c0 1-1 3-2 5c0 0 0 1 0 1c0 0-1 1-2 3c-2 2-5 6-7 7c-1 0-1 1-1 1c-1 0-1 0-2 0c0 0-1 1-2 1c0 1-4 2-6 3c-2 0-4 1-9 2c-3 0-14 1-53 1c-34 0-39 0-40-1zm386 1c0 0-3 0-6 0c-3 0-6-1-6-1c0 0 0-112 0-113c0 0 7 0 40 0c24 0 40 0 41 0c3 1 9 1 10 1c1 0 1 0 2 1c0 0 1 0 2 1c1 0 2 0 3 0c0 0 1 1 2 1c0 1 2 1 2 1c0 0 1 0 1 1c1 0 1 0 1 1c1 0 2 1 4 2c1 0 6 6 7 7c1 1 1 1 1 2c1 1 1 1 1 1c1 0 1 1 1 2c0 0 0 1 1 2c0 0 1 1 1 2c0 1 0 2 0 3c1 2 1 10 0 13c0 0 0 2 0 2c0 0-1 2-1 3c-2 4-3 7-7 10c-2 2-5 4-6 5c-1 0-2 0-2 1c-2 1-5 2-7 3c-2 0-3 1-4 1c-1 0-2 1-3 1c-1 0-2 0-4 0c-2 0-6 1-8 1c-2 0-2 0-3 0c-1 1 0 1 1 2c0 1 2 3 4 5c2 2 5 4 6 5c0 1 3 3 6 5c4 4 8 9 16 16c7 6 12 12 12 12c0 0 0 0-8 1c-9 0-8 0-11-3c-1 0-3-2-4-4c-2-2-6-5-8-8c-3-2-6-5-7-6c-6-5-12-11-18-17c-2-3-6-5-6-6l-2-2l-21 1c-13 0-21 0-21 0c-1 0-1 5-1 22c0 21 0 22 0 22c-1 1-1 1-1 1zm-561-1c0 0 0-26-1-56c0-49 0-57 1-57c0 0 11 0 45 0c25 0 50 0 56 0c9 0 10 0 10 0c0 1 0 1 0 5c0 4 0 5 0 6c0 0-9 0-49 0l-48 0l0 0c-1 1-1 5-1 20c0 18 0 18 1 18c0 1 6 1 42 1c37 0 41 0 42 0c0 1 0 1 0 5c0 4 0 5 0 5c-1 1-4 1-31 1c-16 0-34 0-41 0c-11 0-12 0-12 0c-1 0-1 2-1 21c0 20 0 20 1 21l0 0l49 0c46 0 49 0 49 0c1 1 1 10 0 10c0 1-6 1-56 1c-53 0-56 0-56-1zm725 0c-1 0-1 0 0-2c0 0 1-1 2-2c1-3 2-4 3-6c1-2 2-3 3-4c0-1 1-3 2-4c0 0 1-2 1-2c1 0 1-1 1-2c0 0 1-1 1-1c0-1 1-2 1-3c1 0 2-2 2-2c1-2 4-6 5-9c1 0 1-1 1-1c0 0 0 0 0 0c1-1 2-3 3-4c0-2 1-4 2-5c1 0 1-1 5-7c0-1 1-2 2-3c0-1 0-1 0-1c1 0 1-1 1-2c1 0 1-2 2-2c0-2 1-2 1-3c0-1 1-1 1-2c1 0 1-1 2-3c1-1 2-3 3-4c1-1 3-5 4-7c1-2 2-3 3-5c1-1 1-2 2-2c0-1 1-2 1-3c1-1 2-2 2-2c1-2 3-5 4-7c0 0 1-1 1-2c0 0 1-2 1-2c1-1 2-2 2-2c0-1 0-2 1-2c0 0 0-1 0-1c0 0 1-1 1-1c0-1 1-2 1-2c0 0 1-1 1-1c0-1 13-1 14 0c0 0 0 1 1 1c0 0 1 2 1 3c1 1 3 4 4 6c1 2 3 5 3 5c1 1 1 2 2 3c1 2 2 3 3 5c0 1 1 2 1 2c1 1 1 2 2 3c1 1 2 3 2 3c1 1 2 4 3 6c2 3 4 5 4 6c0 0 0 0 1 1c0 1 1 2 1 3c1 1 2 2 2 2c0 1 3 6 4 6c0 1 2 5 5 10c1 1 2 4 3 6c2 2 3 4 4 6c0 1 1 2 2 3c0 1 1 2 1 2c1 1 1 3 3 4c0 1 1 3 2 3c0 1 0 2 1 2c1 2 3 5 6 10c0 1 1 3 2 4c1 2 2 4 3 4c0 2 1 2 1 3c0 0 1 1 1 1l-1 0l-7 0c-6 0-7 0-7 0c0 0-1 0-1 0c0-1 0-2 0-2c0 0-2-2-2-4c-2-3-3-4-3-4c-1-2-2-3-3-4c-1-2-4-7-4-8c-1-1-1-2-2-3c0-1-1-2-1-2c-1-1-1-1-1-2c-1-1-1-2-2-2l-1-1l-41 0c-26 0-40 0-41 0c0 0-1 1-1 2c0 0-1 1-1 2c-1 1-1 2-2 2c-1 3-2 4-2 4c-1 0-1 1-1 1c0 0 0 1 0 1c-1 0-3 4-6 8c0 1 0 2 0 2c-1 0-2 2-2 2c-1 2-2 3-2 4c-1 1-2 2-2 3c0 1-1 1-1 1c-1 0-13 1-13 0zm205 0c0 0 0-5 0-56c0-46 0-56 0-57c0 0 3 0 55 0c38 0 54 0 54 0c1 0 1 1 1 5c0 5 0 5-1 6c0 0-2 0-48 0l-47 0l-1 0c0 1 0 4 0 20c0 16 0 18 1 18c0 1 4 1 41 1l41 0l1 0l0 1l0 4c0 4 0 5 0 5c0 1-2 1-17 1c-9 0-27 0-41 0c-21 0-25 0-25 0c-1 0-1 1-1 26c0 25 0 26 0 26c-1 0-2 1-6 1c-6 0-6 0-7-1zm219 0c-1 0-1 0-1 0c0 0-1-23-1-51c0-40 0-51 0-51c0 0-6 0-28 0c-25 0-28 0-28 0c-1-1-1-1-1-6c0-4 0-5 1-5c0 0 17 0 64 0c57 0 64 0 64 0c1 1 1 1 1 5c0 4 0 5-1 5l0 1l-12 0c-7 0-20 0-28 0l-16 0l-1 0l-1 1l0 51c0 27 0 50 0 50c0 0 0 0 0 0c-1 0-2 1-6 1c-2-1-5-1-6-1zm-885-11c1 0 3 0 4-1c1 0 2 0 2 0c1 0 1-1 2-1c1 0 2-1 2-1c0 0 1 0 1 0c2-1 4-3 6-4c1-2 2-4 2-4c0-1 1-2 1-2c1-2 1-2 1-6l0-5l-1-3c-1-1-1-2-2-3c-1-1-3-5-5-5c-1-2-4-3-5-3c-1-1-2-1-2-1c-1 0-1 0-2 0c0 0-2-1-3-1c-5-1-10-1-46-1c-16 0-30 0-30 0c0 0-1 0-1 0c0 1 0 10 0 21l0 20l1 1l0 0l37 0c36 0 36 0 38-1zm569-32c1-1 0-2 0-3c0 0-1 0-1-1c-1-1-1-3-3-5c0 0-1-2-1-2c-1-1-1-2-2-3c0-1-1-2-1-2c0-1-1-1-1-2c0 0-1 0-1 0c0-1 0-2-3-6c0-1-1-2-1-3c-1 0-1-2-2-2c0 0-1-2-1-2c-1-1-1-2-2-4c-1-1-2-3-3-4c0 0-1-1-1-2c-1-1-1-2-2-3c0-1-1-2-1-3c-1 0-2-2-2-2c0 0-1-2-2-4c-1-2-2-3-2-3c0 0 0-1-1-1c0 0-1 0-2 2c0 0-1 2-1 2c-2 2-3 5-4 6c-1 3-4 8-5 8c-1 1-1 2-2 4c-1 1-1 2-1 2c0 0-1 0-1 0c0 1 0 2-1 2c0 1-1 2-1 3c-1 1-2 3-3 4c-1 2-2 4-2 4c0 0 0 1-1 1c0 0-1 2-1 2c-1 1-2 3-2 4c-1 1-2 2-2 3c0 1-3 4-4 6c-2 2-2 3-1 3c1 1 3 1 34 1c25 0 33 0 33 0zm-206-13c5 0 7-1 8-1c1 0 2-1 3-1c3 0 10-4 12-6c0 0 1-2 1-2c1 0 2-2 2-2c1-2 1-3 2-6c0-2 0-6 0-8c0-6-4-10-8-14c-2-1-6-3-8-4c-5-1-6-2-12-2c-1 0-16 0-33 0c-28 0-31 0-31 0c-1 1-1 2-1 23c0 19 0 22 1 23c0 0 1 0 28 0c16 0 30 0 30 0c1 0 3 0 6 0zm-366-8c1 0 3 0 4-1c0 0 2 0 2-1c1 0 2 0 2 0c1 0 1-1 2-1c0 0 1-1 2-1c3-2 5-5 6-8l1-2l0-4l0-5l-1-2c0-1-1-3-1-3c-1-2-4-4-6-6c-2 0-5-2-7-2c0 0-1 0-2-1c-1 0-2-1-3-1c-1 0-3 0-5 0c-3 0-10 0-35 0c-30 0-31 0-31 0c-1 1-1 2-1 19c0 13 0 19 0 19c1 0 1 0 1 0c0 0 16 0 34 0c30 0 35 0 38 0z'

FONTS = 'https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=Spectral:ital,wght@0,300;0,400;0,500;1,400&display=swap'

def head(title, desc, d, canonical):
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F3F5F8">
<link rel="canonical" href="{DOMAIN}/{canonical}">
<link rel="icon" href="{d}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="ГалА-Консалт">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{DOMAIN}/assets/img/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{d}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">К содержанию</a>
'''

NAV = [('about', 'О компании'), ('services', 'Услуги'), ('projects', 'Проекты'), ('management', 'Руководство'), ('contacts', 'Контакты')]

def header(d, home):
    pre = '' if home else f'{d}index.html'
    links = ''.join(f'<a href="{pre}#{k}"' + (' class="is-active" aria-current="page"' if (not home and k == 'projects') else '') + f'>{v}</a>' for k, v in NAV)
    return f'''<header class="hdr" id="top">
  <div class="wrap hdr__in">
    <a class="brand" href="{d}index.html" aria-label="ГалА-Консалт, на главную"><img src="{d}assets/img/logo-h.svg" alt="GalA-Consult · ГалА-Консалт" width="256" height="64"></a>
    <nav class="nav" aria-label="Разделы">{links}</nav>
    <div class="hdr__cta">
      <a class="hdr__tel" href="tel:+77015509900">+7 701 550-99-00</a>
      <a class="btn btn--sm" href="{pre}#contacts" data-form>Связаться</a>
    </div>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Открыть меню"><span></span></button>
  </div>
</header>
<div class="menu" id="menu" hidden>
  <nav aria-label="Меню">{links}</nav>
  <div class="menu__contacts">
    <a href="tel:+77015509900">+7 701 550-99-00</a>
    <a href="tel:+77272501139">+7 727 250-11-39</a>
    <a href="mailto:gaco@galaconsult.kz">gaco@galaconsult.kz</a>
    <span>ул. Жамбыла, 26, Алматы</span>
  </div>
</div>
'''

def footer(d, home):
    pre = '' if home else f'{d}index.html'
    links = ''.join(f'<a href="{pre}#{k}">{v}</a>' for k, v in NAV)
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <a class="ftr__logo" href="{d}index.html" aria-label="ГалА-Консалт, на главную"><img src="{d}assets/img/logo-full.svg" alt="GalA-Consult · ГалА-Консалт" width="360" height="133" loading="lazy"></a>
      <div class="ftr__col"><h3>Разделы</h3>{links}</div>
      <div class="ftr__col"><h3>Контакты</h3>
        <span>ул. Жамбыла, 26, Алматы, Казахстан</span>
        <a href="tel:+77272501139">+7 727 250-11-39</a>
        <a href="tel:+77015509900">+7 701 550-99-00</a>
        <a href="mailto:gaco@galaconsult.kz">gaco@galaconsult.kz</a>
        <a href="mailto:info@galaconsult.kz">info@galaconsult.kz</a>
      </div>
    </div>
    <div class="ftr__bottom">
      <span>© 2026 ТОО «ГалА-Консалт» · GalA-Consult LLP</span>
      <a class="wc" href="https://wwwebcraft.com" target="_blank" rel="noopener"><span>Made by</span><svg viewBox="0 0 1521 119.25" role="img" aria-label="WEBCRAFT"><defs><linearGradient id="wc-g"><stop offset="0" stop-color="#F0B57F"/><stop offset=".5" stop-color="#B9AEF4"/><stop offset="1" stop-color="#7CA3EE"/></linearGradient></defs><use href="#wc"/><use class="wc-h" href="#wc" fill="url(#wc-g)"/></svg></a>
      <a class="ftr__top" href="#top">Наверх{I['up']}</a>
    </div>
  </div>
</footer>
{request_modal(d)}
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><symbol id="wc" viewBox="0 0 1521 119.25"><path fill-rule="evenodd" d="{WC_D}"/></symbol></svg>
<script src="{d}assets/js/site.js" defer></script>
</body>
</html>
'''

TOPICS = ['Право, налоги, таможня', 'Выход на рынок', 'Международные связи', 'Обучение и коммуникация', 'Участие в проекте', 'Другое']

def request_modal(d):
    chips = ''.join(f'<label class="chip-r"><input type="radio" name="topic" id="rq-t{i + 1}" value="{t}"><span>{t}</span></label>' for i, t in enumerate(TOPICS))
    return f'''<div class="modal" id="rq" role="dialog" aria-modal="true" aria-labelledby="rq-title" hidden>
  <div class="modal__bg" data-close></div>
  <div class="modal__panel">
    <button class="modal__x" type="button" data-close aria-label="Закрыть">{I['x']}</button>
    <form class="rq" name="request" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>
      <input type="hidden" name="form-name" value="request">
      <input type="hidden" name="project" value="">
      <input type="hidden" name="page" value="">
      <input type="hidden" name="subject" value="Запрос с сайта galaconsult.kz">
      <p class="hp"><label>Не заполняйте это поле <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="rq__head">
        <img class="rq__logo" src="{d}assets/img/logo-h.svg" alt="" width="128" height="32">
        <h2 class="rq__title" id="rq-title">Написать нам</h2>
        <p class="rq__sub">Оставьте контакты и выберите тему. Мы свяжемся с вами, чтобы обсудить задачу.</p>
      </div>
      <div class="field" id="f-name"><input id="rq-name" name="name" type="text" autocomplete="name" placeholder=" " required><label for="rq-name">Имя</label><span class="field__err" aria-live="polite"></span></div>
      <div class="field" id="f-company"><input id="rq-company" name="company" type="text" autocomplete="organization" placeholder=" "><label for="rq-company">Предприятие / компания</label></div>
      <div class="field" id="f-contact"><input id="rq-contact" name="contact" type="text" autocomplete="tel" placeholder=" " required><label for="rq-contact">Телефон или email</label><span class="field__err" aria-live="polite"></span></div>
      <fieldset class="topics" id="f-topic"><legend>Тема запроса</legend><div class="topics__list">{chips}</div><span class="topics__err" aria-live="polite"></span></fieldset>
      <button class="btn rq__send" type="submit">Отправить запрос</button>
      <p class="rq__fail" hidden>Не получилось отправить запрос. Позвоните нам: <span class="nw">+7 701 550-99-00</span> или напишите на gaco@galaconsult.kz</p>
      <p class="rq__note">Отправляя запрос, вы соглашаетесь на обработку указанных данных для ответа на него.</p>
    </form>
    <div class="fx" aria-hidden="true">
      <svg class="fx__trail" viewBox="0 0 580 640"><path d="M290,358 C371,346 487,256 545,38" pathLength="1"/></svg>
      <div class="fx__env">
        <div class="fx__back"></div>
        <div class="fx__letter"><img src="{d}assets/img/logo-h.svg" alt=""><b data-fx="topic"></b><span data-fx="name"></span><span data-fx="company"></span><i></i><i></i></div>
        <div class="fx__pocket"></div>
        <div class="fx__flap"></div>
        <div class="fx__seal">{logos.seal_mark()}</div>
      </div>
    </div>
    <div class="done" role="status" hidden>
      <svg class="done__ring" viewBox="0 0 88 88" aria-hidden="true"><defs><linearGradient id="doneG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFC9A0"/><stop offset=".5" stop-color="#E8722C"/><stop offset="1" stop-color="#A9481A"/></linearGradient></defs><circle cx="44" cy="44" r="40" pathLength="1"/><path d="M28 45l11 11 22-24" pathLength="1"/></svg>
      <h3>Запрос отправлен</h3>
      <p>Спасибо, <span data-fx="who"></span>. Мы получили ваш запрос и свяжемся с вами по указанным контактам.</p>
      <button class="btn" type="button" data-close>Готово</button>
    </div>
  </div>
</div>'''

def place(p, d):
    return f'<span class="place"><img src="{d}assets/img/flags/{p["flag"]}.svg" alt="" width="22" height="15">{p["place"]}</span>'

def proj_card(p, d):
    return f'''<a class="proj" href="{d}projects/{p['slug']}.html">
  <div class="proj__top"><span class="tag">{p['type']}</span>{place(p, d)}</div>
  <div class="proj__date">{p['dates']}</div>
  <h3 class="proj__title">{p['short']}</h3>
  <div class="proj__foot"><span class="proj__docs">{I['clip']}2 документа</span><span class="proj__more">Подробнее{I['arrow']}</span></div>
</a>'''

# ---------------- hero lockup ----------------
def hero_lockup():
    return (f'<div class="lockup rise rise-3" role="img" aria-label="GalA-Consult · ГалА-Консалт">'
            f'<svg viewBox="{logos.FULL_VB}" aria-hidden="true">{logos.full_inner("hx", sheen=True)}</svg></div>')

# ---------------- map ----------------
def geo_map(d):
    W, H, C = MAP['W'], MAP['H'], MAP['cities']
    ax, ay = C['almaty']
    dests = [('munich', .30, 0), ('dresden', .36, 1.1), ('vienna', .25, 2.3), ('zurich', .28, 3.2), ('bolzano', .21, 4.4), ('istanbul', .17, 5.4)]
    arcs, dots, marks = '', '', ''
    for key, h, begin in dests:
        bx, by = C[key]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        if ny > 0: nx, ny = -nx, -ny
        cx, cy = (ax + bx) / 2 + nx * L * h, (ay + by) / 2 + ny * L * h
        path = f'M{ax},{ay}Q{cx:.1f},{cy:.1f} {bx},{by}'
        arcs += f'<path d="{path}" class="route" pathLength="1"/>'
        dots += (f'<circle r="3.4" class="route-dot" fill="#E8722C" opacity="0"><animateMotion dur="6.5s" begin="{begin}s" repeatCount="indefinite" path="{path}" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".45 0 .25 1"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.82;1" dur="6.5s" begin="{begin}s" repeatCount="indefinite"/></circle>')
        if key != 'istanbul':
            marks += f'<circle cx="{bx}" cy="{by}" r="4" fill="#fff" stroke="#2453D0" stroke-width="2"/>'
    ix, iy = C['istanbul']
    marks += f'<circle cx="{ix}" cy="{iy}" r="4.5" fill="#fff" stroke="#2453D0" stroke-width="2"/>'
    marks += (f'<circle cx="{ax}" cy="{ay}" r="7" fill="none" stroke="#E8722C" stroke-width="1.6"><animate attributeName="r" values="7;26" dur="2.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".55;0" dur="2.8s" repeatCount="indefinite"/></circle>'
              f'<circle cx="{ax}" cy="{ay}" r="7" fill="#0E2650" stroke="#fff" stroke-width="2.5"/>')
    # leader from label to the cluster
    lx, ly = 300, 196
    marks += f'<path d="M{lx},{ly + 4}L{lx + 8},{ly + 30}" stroke="#2453D0" stroke-width="1.2" stroke-dasharray="2 3" fill="none"/>'
    pct = lambda x, y, oy=0: f'left:{x / W * 100:.2f}%;top:{(y + oy) / H * 100:.2f}%'
    labels = (f'<span class="geo-lbl geo-lbl--home geo-lbl--end" style="{pct(ax, ay, -16)}">Алматы</span>'
              f'<span class="geo-lbl geo-lbl--left" style="{pct(ix, iy)}">Стамбул</span>'
              f'<span class="geo-lbl geo-lbl--multi" style="{pct(lx, ly)}"><small>Немецкоязычная Европа</small>Германия, Австрия, Швейцария, Южный Тироль</span>')
    return f'''<div class="geo-map settle" role="img" aria-label="Карта: маршруты из Алматы в Германию, Австрию, Швейцарию, Южный Тироль и Стамбул">
  <div class="geo-map__in">
    <img src="{d}assets/img/map-dots.svg" alt="" width="1200" height="540" loading="lazy">
    <svg viewBox="0 0 {W} {H}" data-smil aria-hidden="true">
      <defs><linearGradient id="routeG" gradientUnits="userSpaceOnUse" x1="{ax}" y1="0" x2="300" y2="0"><stop offset="0" stop-color="#0E2650" stop-opacity=".9"/><stop offset="1" stop-color="#2453D0" stop-opacity=".75"/></linearGradient></defs>
      <g fill="none" stroke="url(#routeG)" stroke-width="1.6" stroke-linecap="round">{arcs}</g>
      {dots}{marks}
    </svg>
    {labels}
  </div>
</div>'''

def flags_row(d):
    items = [('kz', 'Казахстан', 'Алматы'), ('de', 'Германия', 'Бавария, Саксония'), ('at', 'Австрия', ''), ('ch', 'Швейцария', ''), ('st', 'Южный Тироль', 'Италия')]
    out = ''
    for code, name, sub in items:
        subh = f'<small>{sub}</small>' if sub else ''
        out += (f'<li class="pole"><span class="pole__mast" aria-hidden="true"></span>'
                f'<div class="flag" data-src="{d}assets/img/flags/{code}.svg"><img src="{d}assets/img/flags/{code}.svg" alt="" width="180" height="120" loading="lazy"><canvas aria-hidden="true"></canvas></div>'
                f'<span class="pole__name">{name}{subh}</span></li>')
    return f'<ul class="flags" aria-label="Страны">{out}</ul>'

# ---------------- home ----------------
def home():
    d = ''
    recent = P[:3]
    svc = [
        ('law', 'Право, налоги, таможня', ['Консультации, информация и услуги по юридическим, налоговым, таможенным и общим экономическим вопросам', 'Сопровождение проектов']),
        ('market', 'Выход на рынок', ['Создание фирм, представление фирм на рынке', 'Маркетинговые исследования', 'Межкультурная информация']),
        ('globe', 'Международные связи', ['Содействие в установлении деловых контактов между предпринимателями Казахстана и иностранными партнерами', 'Организация, сопровождение экономических делегаций', 'Поддержка казахстанских компаний в сотрудничестве с партнерами из Германии, Австрии, Швейцарии и Южного Тироля']),
        ('talk', 'Обучение и коммуникация', ['Организация семинаров по вопросам деловой активности и ведения бизнеса в Казахстане', 'Обучение кадров', 'Устные и письменные переводы']),
    ]
    svc_html = ''.join(f'<article class="svc"><div class="svc__top"><span class="coin">{I[i]}</span><h3 class="h3">{t}</h3></div><ul class="svc__list">{"".join(f"<li>{x}</li>" for x in items)}</ul><button class="svc__cta" type="button" data-form data-topic="{t}">Обсудить задачу{I["arrow"]}</button></article>' for i, t, items in svc)
    approach = [('book', 'Глубокие знания и практический опыт в правовой, экономической и социально-политической областях'),
                ('flow', 'Понимание бизнес-процессов, в которых клиенты осуществляют свою деятельность'),
                ('people', 'Учет менталитета иностранных деловых партнеров')]
    appr_html = ''.join(f'<li class="approach__item"><span class="coin coin--sm">{I[i]}</span><p>{t}</p></li>' for i, t in approach)
    career = [('с 1994 года', 'Глава Представительства Германской экономики в Казахстане'),
              ('', 'Заместитель главы Представительства Германской экономики в Центральной Азии'),
              ('', 'Генеральный директор сервисной компании ТОО «DEinternational Kasachstan»'),
              ('с основания', 'Член Правления Клуба Германской экономики, затем Союза Германской экономики в Республике Казахстан'),
              ('сегодня', 'Учредитель и управляющий партнер ТОО «ГалА-Консалт»')]
    career_html = ''.join(f'<li><span class="career__when">{w}</span><span class="career__what">{t}</span></li>' for w, t in career)
    cards = ''.join(proj_card(p, d) for p in recent)
    body = f'''{header(d, True)}<main id="main">
<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__text">
      <p class="label rise">Консалтинговая компания · Алматы</p>
      <h1 class="display rise rise-2">Консалтинг и деловые связи между Казахстаном и немецкоязычной Европой</h1>
      <p class="lead rise rise-3">Консультируем казахстанские и иностранные компании по юридическим, налоговым, таможенным и общеэкономическим вопросам. Организуем деловые поездки, делегации и посещение отраслевых выставок в Германии, Австрии, Швейцарии и других странах.</p>
      <div class="hero__actions rise rise-4"><a class="btn" href="#contacts" data-form>Получить консультацию</a><a class="link-arrow" href="#projects">Смотреть проекты{I['arrow']}</a></div>
    </div>
    {hero_lockup()}
  </div>
  <div class="wrap facts rise rise-5">
    <div class="facts__row">
      <div class="fact"><span class="fact__num">1994</span><p class="fact__txt">С этого года основатель компании возглавляла Представительство Германской экономики в Казахстане</p></div>
      <div class="fact"><span class="fact__num">23</span><p class="fact__txt">года деятельности основателя в области казахстанско-германских экономических отношений</p></div>
      <div class="fact"><span class="fact__num">4</span><p class="fact__txt">немецкоязычных направления: Германия, Австрия, Швейцария, Южный Тироль</p></div>
    </div>
  </div>
</section>

<section class="sec sec--paper sec--rule" id="about">
  <div class="wrap split">
    <div class="split__head"><p class="label">О компании</p><h2 class="h2">Комплексное сопровождение бизнеса и разовые консультации</h2>
      <div class="approach"><p class="approach__title">Наш подход</p><ul class="approach__list">{appr_html}</ul></div>
    </div>
    <div class="split__body">
      <p class="lead">ТОО «ГалА-Консалт» предлагает информационные и консалтинговые услуги по юридическим, налоговым, таможенным и общеэкономическим вопросам как в рамках комплексного сопровождения бизнеса, так и в форме проведения разовых консультаций.</p>
      <p>Помимо этого мы оказываем такие необходимые услуги, как маркетинговые исследования, организация и сопровождение экономических делегаций, устные и письменные переводы.</p>
      <p>Мы предоставляем консалтинговые услуги казахстанским и иностранным предприятиям в Центральной Азии, а также информируем и консультируем местные предприятия о возможностях делового сотрудничества в Германии, Австрии, Швейцарии и других странах.</p>
    </div>
  </div>
</section>

<section class="sec" id="services">
  <div class="wrap">
    <div class="sec__head"><p class="label">Услуги</p><h2 class="h2">Чем мы помогаем компаниям</h2><p class="sec__note">Работаем в формате комплексного сопровождения или берем отдельную задачу, от разовой консультации до организации делегации.</p></div>
    <div class="svc-grid">{svc_html}</div>
  </div>
</section>

<section class="sec sec--paper" id="projects">
  <div class="wrap">
    <div class="sec__head sec__head--row"><div><p class="label">Проекты</p><h2 class="h2">Деловые поездки, делегации и выставки</h2></div><a class="link-arrow" href="projects/index.html">Проекты{I['arrow']}</a></div>
    <div class="proj-grid">{cards}</div>
  </div>
</section>

<section class="sec" id="management">
  <div class="wrap founder">
    <figure class="photo settle"><div class="photo__frame"><img src="assets/img/founder.jpg" alt="Доктор Галия Джунусалиева на деловом заседании" width="630" height="575" loading="lazy"></div><figcaption>Доктор Галия Сагадиновна Джунусалиева</figcaption></figure>
    <div class="founder__body">
      <p class="label">Руководство</p>
      <h2 class="h2">Доктор Галия Джунусалиева</h2>
      <p class="founder__role">Учредитель и управляющий партнер</p>
      <p class="lead">Главный специалист компании. Имеет огромный опыт и специальные знания в области консалтинговых услуг.</p>
      <ul class="career">{career_html}</ul>
      <p class="founder__note">После 23-летней деятельности в области казахстанско-германских экономических отношений Г. Джунусалиева возобновила свою деятельность в компании ТОО «ГалА-Консалт».</p>
    </div>
  </div>
</section>

<section class="sec sec--paper" id="geography">
  <div class="wrap">
    <div class="sec__head sec__head--row"><div><p class="label">География</p><h2 class="h2">Казахстан и немецкоязычная Европа</h2></div><p class="sec__note">Информируем казахстанские предприятия о возможностях сотрудничества в Германии, Австрии, Швейцарии и Южном Тироле и сопровождаем делегации на выставки и встречи с партнерами.</p></div>
    {geo_map(d)}
    {flags_row(d)}
  </div>
</section>

<section class="contacts" id="contacts">
  <div class="wrap contacts__grid">
    <div class="contacts__intro">
      <p class="label label--light">Контакты</p>
      <h2 class="h2">Свяжитесь с нами</h2>
      <p>Ответим на вопросы о консультациях, деловых поездках и участии в делегациях.</p>
      <a class="btn btn--light" href="mailto:gaco@galaconsult.kz" data-form>{I['mail']}Написать письмо</a>
    </div>
    <dl class="cinfo">
      <div class="cinfo__row"><dt>Адрес</dt><dd><span class="cinfo__line" id="c-addr">ул. Жамбыла, 26, Алматы, Казахстан</span>
        <span class="cinfo__links"><a class="chip" href="https://2gis.kz/almaty/search/%D0%96%D0%B0%D0%BC%D0%B1%D1%8B%D0%BB%D0%B0%2026" target="_blank" rel="noopener">{I['pin']}2ГИС</a><a class="chip" href="https://www.google.com/maps/search/?api=1&amp;query=%D0%96%D0%B0%D0%BC%D0%B1%D1%8B%D0%BB%D0%B0+26+%D0%90%D0%BB%D0%BC%D0%B0%D1%82%D1%8B" target="_blank" rel="noopener">{I['pin']}Google Карты</a></span></dd></div>
      <div class="cinfo__row"><dt>Телефоны</dt><dd>
        <span class="cinfo__line"><a href="tel:+77015509900" id="c-tel1">+7 701 550-99-00</a><button class="copy" type="button" data-copy="+7 701 550-99-00" aria-controls="c-tel1" aria-label="Скопировать">{I['copy']}</button></span>
        <span class="cinfo__line"><a href="tel:+77272501139" id="c-tel2">+7 727 250-11-39</a><button class="copy" type="button" data-copy="+7 727 250-11-39" aria-controls="c-tel2" aria-label="Скопировать">{I['copy']}</button></span></dd></div>
      <div class="cinfo__row"><dt>Почта</dt><dd>
        <span class="cinfo__line"><a href="mailto:gaco@galaconsult.kz" id="c-m1">gaco@galaconsult.kz</a><button class="copy" type="button" data-copy="gaco@galaconsult.kz" aria-controls="c-m1" aria-label="Скопировать">{I['copy']}</button></span>
        <span class="cinfo__line"><a href="mailto:info@galaconsult.kz" id="c-m2">info@galaconsult.kz</a><button class="copy" type="button" data-copy="info@galaconsult.kz" aria-controls="c-m2" aria-label="Скопировать">{I['copy']}</button></span></dd></div>
    </dl>
  </div>
</section>
</main>
{footer(d, True)}'''
    title = 'ГалА-Консалт · консалтинг и деловые связи с Германией, Австрией и Швейцарией'
    desc = 'ТОО «ГалА-Консалт», Алматы: юридические, налоговые и таможенные консультации, деловые поездки, делегации и выставки в Германии, Австрии и Швейцарии.'
    return head(title, desc, d, ''), body

# ---------------- project page ----------------
def doc_row(doc, idx=None):
    title, ext, url, sub = doc
    ext_l = ext.upper()
    num = f'Приложение {idx}. ' if idx else ''
    inner = (f'<span class="doc__file">{DOCFILE}<span class="doc__ext doc__ext--{ext}">{ext_l}</span></span>'
             f'<span class="doc__text"><span class="doc__title">{num}{title}</span><span class="doc__sub">{sub}</span></span>')
    if url:
        return f'<li><a class="doc" href="{url}" target="_blank" rel="noopener">{inner}<span class="doc__go">{I["ext"]}</span></a></li>'
    return f'<li><div class="doc doc--pending">{inner}<span class="doc__soon">скоро</span></div></li>'

def project_page(i):
    p = P[i]; d = '../'
    blocks = ''
    for kind, val in p['body']:
        if kind == 'p': blocks += f'<p>{val}</p>'
        elif kind == 'salute': blocks += f'<p class="salute">{val}</p>'
        elif kind == 'h3': blocks += f'<h3>{val}</h3>'
        elif kind == 'ul': blocks += '<ul>' + ''.join(f'<li>{x}</li>' for x in val) + '</ul>'
        elif kind == 'callout': blocks += f'<p class="callout">{val}</p>'
    sign = '<div class="letter__sign">С уважением и наилучшими пожеланиями,<b>ТОО «ГалА-Консалт»</b></div>' if p.get('sign') else '<div class="letter__sign">По вопросам участия: gaco@galaconsult.kz, info@galaconsult.kz, <span class="nw">+7 701 550-99-00</span><b>ТОО «ГалА-Консалт»</b></div>'
    docs_att = ''.join(doc_row(x, n + 1) for n, x in enumerate(p['docs']))
    docs_side = ''.join(doc_row(x) for x in p['docs'])
    kv = [('Даты', p['dates']), ('Место', p['place'] + (f'<br><span class="muted">{p["venue"]}</span>' if p.get('venue') else '')), ('Формат', p['type']), ('Тема', p['topic'])]
    if p.get('program'): kv.append(('Программа', p['program']))
    if p.get('deadline'): kv.append(('Анкета до', p['deadline']))
    kv_html = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in kv)
    theme = f'<p class="pp__theme"><b>Тема:</b><span>{p["theme"]}</span></p>' if p.get('theme') else ''
    older = P[i + 1] if i + 1 < len(P) else None
    newer = P[i - 1] if i > 0 else None
    left = (f'<a class="pnav" href="{older["slug"]}.html"><span class="pnav__dir">← Предыдущий проект</span><span class="pnav__t">{older["short"]}</span></a>' if older
            else '<a class="pnav" href="index.html"><span class="pnav__dir">← Все проекты</span><span class="pnav__t">Архив поездок и делегаций</span></a>')
    right = (f'<a class="pnav pnav--next" href="{newer["slug"]}.html"><span class="pnav__dir">Следующий проект →</span><span class="pnav__t">{newer["short"]}</span></a>' if newer
             else '<a class="pnav pnav--next" href="index.html"><span class="pnav__dir">Все проекты →</span><span class="pnav__t">Архив поездок и делегаций</span></a>')
    body = f'''{header(d, False)}<main id="main">
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигация"><a href="../index.html">Главная</a><span>/</span><a href="index.html">Проекты</a><span>/</span><span aria-current="page">{p['year']}</span></nav>
    <header class="pp__head">
      <div class="pp__meta"><span class="pill">{p['type']}</span><span class="pp__date">{p['dates']}</span>{place(p, d)}</div>
      <h1 class="pp__title">{p['title']}</h1>
      {theme}
    </header>
    <div class="pp__grid">
      <article class="letter">
        <div class="letter__head"><img src="../assets/img/logo-full.svg" alt="GalA-Consult · ГалА-Консалт" width="300" height="111"><p class="letter__addr">ТОО «ГалА-Консалт»<br>ул. Жамбыла, 26, Алматы<br>gaco@galaconsult.kz · <span class="nw">+7 727 250-11-39</span></p></div>
        <div class="letter__body">{blocks}</div>
        {sign}
        <div class="attach" id="documents"><p class="attach__title">Приложения</p><ul class="docs">{docs_att}</ul></div>
      </article>
      <aside class="pp__side">
        <div class="side side--docs"><p class="side__title">Документы</p><ul class="docs">{docs_side}</ul></div>
        <div class="side"><p class="side__title">Коротко</p><dl class="kv">{kv_html}</dl></div>
        <div class="side side--ask"><p class="side__title">Вопросы по участию</p><div class="ask"><a href="mailto:gaco@galaconsult.kz">gaco@galaconsult.kz</a><a href="mailto:info@galaconsult.kz">info@galaconsult.kz</a><a href="tel:+77015509900">+7 701 550-99-00</a></div><a class="btn btn--sm" href="mailto:gaco@galaconsult.kz" data-form data-topic="Участие в проекте" data-project="{E(p['short'])}">Задать вопрос</a></div>
      </aside>
    </div>
    <nav class="pp__nav" aria-label="Другие проекты">{left}{right}</nav>
  </div>
</main>
{footer(d, False)}'''
    plain = re.sub('<[^>]+>', '', p['title'])
    return head(f'{p["short"]} · ГалА-Консалт', E(plain + ', ' + p['dates'] + '. ТОО «ГалА-Консалт».'), d, f'projects/{p["slug"]}'), body

def archive():
    d = '../'
    years = sorted({p['year'] for p in P}, reverse=True)
    out = ''
    for y in years:
        rows = ''.join(f'''<a class="reg__row" href="{d}projects/{p['slug']}.html"><span class="reg__when"><span class="reg__date">{p['dates']}</span><span class="tag">{p['type']}</span></span><span class="reg__t">{p['short']}</span>{place(p, d)}<span class="reg__go">{I['arrow']}</span></a>''' for p in P if p['year'] == y)
        out += f'<section class="year"><h2 class="year__n">{y}</h2><div class="reg">{rows}</div></section>'
    body = f'''{header(d, False)}<main id="main">
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигация"><a href="../index.html">Главная</a><span>/</span><span aria-current="page">Проекты</span></nav>
    <header class="arch-head"><p class="label">Проекты</p><h1 class="display" style="font-size:clamp(36px,4.4vw,60px)">Деловые поездки, делегации и выставки</h1><p class="lead">Программы для казахстанских предприятий в Германии, Турции и других странах. На странице каждого проекта - описание, даты и документы для участников.</p></header>
    <div style="padding-bottom:clamp(56px,7vw,96px)">{out}</div>
  </div>
</main>
{footer(d, False)}'''
    return head('Проекты · ГалА-Консалт', 'Деловые поездки, делегации и выставки, которые организует ТОО «ГалА-Консалт».', d, 'projects/'), body

def not_found():
    # served by Netlify for any missing path, so every link and asset is root-absolute
    d = '/'
    cards = ''.join(proj_card(p, d) for p in P[:3])
    body = f'''{header(d, False)}<main id="main">
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигация"><a href="/">Главная</a><span>/</span><span aria-current="page">Страница не найдена</span></nav>
    <header class="arch-head"><p class="label">Ошибка 404</p><h1 class="display" style="font-size:clamp(36px,4.4vw,60px)">Такой страницы нет</h1><p class="lead">Возможно, ссылка устарела или страница переехала. Последние проекты - ниже, полный список - в разделе «Проекты».</p>
      <div class="hero__actions"><a class="btn" href="/projects/">Все проекты</a><a class="link-arrow" href="/">На главную{I['arrow']}</a></div></header>
    <div class="proj-grid" style="padding-bottom:clamp(56px,7vw,96px)">{cards}</div>
  </div>
</main>
{footer(d, False)}'''
    body = body.replace(' class="is-active" aria-current="page"', '')
    h = head('Страница не найдена · ГалА-Консалт', 'Страница не найдена. ТОО «ГалА-Консалт».', d, '')
    h = re.sub(r'<link rel="canonical"[^>]*>', '<meta name="robots" content="noindex">', h)
    return h, body

def write(rel, h, b):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(h + b)

h, b = home()
write('index.html', h, b)
# artifact entry page: same content, without the document skeleton tags
art_head = h.replace('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n', '')
art_head = art_head.replace('</head>\n<body>\n', '\n')
art_head = re.sub(r'<title>[^<]*</title>', '<title>GalA-Consult</title>', art_head, count=1)
art_body = b.replace('</body>\n</html>\n', '')
# claude.ai preview entry (not deployed, kept out of git)
ART = os.path.join(ROOT, 'artifact')
os.makedirs(ART, exist_ok=True)
open(os.path.join(ART, 'index.html'), 'w').write(art_head + art_body)
for i in range(len(P)):
    h2, b2 = project_page(i)
    write(f'projects/{P[i]["slug"]}.html', h2, b2)
h3, b3 = archive()
write('projects/index.html', h3, b3)
h4, b4 = not_found()
write('404.html', h4, b4)
# netlify redirects for old links, sitemap, robots
open(os.path.join(SITE, '_redirects'), 'w').write(''.join(f'/{o}  /projects/{n}  301\n' for o, n in OLD_SLUGS.items()))
urls = [''] + ['projects/'] + [f'projects/{p["slug"]}' for p in P]
open(os.path.join(SITE, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(SITE, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
print('built', len(P) + 3, 'pages')
