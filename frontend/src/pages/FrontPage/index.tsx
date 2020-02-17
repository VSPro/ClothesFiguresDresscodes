import React, { Fragment } from 'react';
import { CssBaseline, Container } from '@material-ui/core';
import MainContent from './MainContent/index';
import MainLayout from '../../modules/MainLayout';
import HowItWorksContent from './HowItWorksContent/index';
import ServicePurposeContent from './ServicePurposeContent';
import FigureTypeContent from './FigureTypeContent';
import ClothesStylesContetn from './ClothesStylesContent';

const mainContent = {
  title: 'Сервис-помощник по подбору одежды',
  description:
    'Мы не продаем, мы помогаем подобрать одежду с учетом особенностей фигруы, внешности и под стать обстановке',
  img1: 'https://cs.pikabu.ru/images/big_size_comm/2012-10_4/13504737395385.gif',
  img2: 'https://cs.pikabu.ru/images/big_size_comm/2012-10_4/13504737395385.gif',
  firstBtnText: 'Начать новый подбор',
  secondBtnText: 'Продолжить подбор',
};

const howItWorksContent = {
  title: 'Как это работает',
  steps: [
    { id: 1, title: 'Снимите мерки со своей фигуры' },
    { id: 2, title: 'Добавьте особенности своей внешности' },
    { id: 3, title: 'Получите заключение по типу вашей фигуры' },
    { id: 4, title: 'Отметьте нужные фильтры одежды' },
    { id: 5, title: 'Выберите одежду, из подобранной сервисом' },
    { id: 6, title: 'Добавьте выще в корзину и соверщайте покупки' },
  ],
  btnText: 'Определить тип фигуры',
};

const servicePurposeContent = {
  title: 'Основная цель сервиса',
  description:
    'Не у каждого человека модельные параметры. Подходит ли под вашу фигуру выбранная в магазине вещь? Подходит ли она нашему возрасту статусу? Наш сайт поможет подобрать одежду с учетом вашей внешности и друсс-кода.',
  btnText: 'Подробнее',
};

const figureTypeContent = {
  title: 'Типы фигур',
  description:
    'Кто-то коренастый, кто-то вытянутый. Не каждый костюмчик будет сидеть на всех одинаково.Фигуры людей можно распределить по группам, на основе снимаемых мерок.Сервис определяет основные характеристики внешности, для дальнейшего подбора одежды.',
  btnText: 'Подробнее',
};

const clothesStylesContent = {
  title: 'Стили одежды',
  description:
    'Одежда должна не только хорошо подходить вам, также она должна подходить мероприятию, на которое вы собираетесь. Здесь помогает понятие о дресс-кодах.Вы можете выбрать желаемый дресс-код и получать в раздаче только соответствующую ему одежду.',
  btnText: 'Подробнее',
};

export default function FrontPage() {
  return (
    <Fragment>
      <CssBaseline />
      <Container>
        <MainLayout>
          <MainContent content={mainContent} />
          <HowItWorksContent content={howItWorksContent} />
          <ServicePurposeContent content={servicePurposeContent} />
          <FigureTypeContent content={figureTypeContent} />
          <ClothesStylesContetn content={clothesStylesContent} />
        </MainLayout>
      </Container>
    </Fragment>
  );
}
