import React, { Fragment } from 'react';
import { CssBaseline, Container } from '@material-ui/core';
import MainContent from './MainContent/index';
import MainLayout from '../../modules/MainLayout';
import HowItWorksContent from './HowItWorksContent/index';
import ServicePurposeContent from './ServicePurposeContent';

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
  description: '',
  btnText: '',
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
        </MainLayout>
      </Container>
    </Fragment>
  );
}
