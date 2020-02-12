import React, { Fragment } from 'react';
import { CssBaseline, Container } from '@material-ui/core';
import Footer from './Footer';
import Header from './Header';
import MainFeaturedPost from './MainFeaturedPost';

const sections = [
  { title: 'О СЕРВИСЕ', url: '#' },
  { title: 'ОЦЕНКА ФИГУРЫ', url: '#' },
  { title: 'КАК СНИМАТЬ МЕРКИ', url: '#' },
  { title: 'ТИРЫ ФИГУР', url: '#' },
  { title: 'ПОДБОР ОДЕЖДЫ', url: '#' },
  { title: 'bucket', url: '#', img: '' },
];

const mainFeaturedPost = {
  title: 'Сервис-помощник по подбору одежды',
  description:
    'Мы не продаем, мы помогаем подобрать одежду с учетом особенностей фигруы, внешности и под стать обстановке',
  img1: 'https://cs.pikabu.ru/images/big_size_comm/2012-10_4/13504737395385.gif',
  img2: 'https://cs.pikabu.ru/images/big_size_comm/2012-10_4/13504737395385.gif',
  firstBtnText: 'Начать новый подбор',
  secondBtnText: 'Продолжить подбор',
};

export default function FrontPage() {
  return (
    <Fragment>
      <CssBaseline />
      <Container>
        <Header sections={sections} />
        <MainFeaturedPost mainFeaturedPost={mainFeaturedPost} />
      </Container>
      <Footer />
    </Fragment>
  );
}
