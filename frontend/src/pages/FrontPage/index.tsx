import React, { Fragment } from 'react';
import { CssBaseline, Container } from '@material-ui/core';
import MainFeaturedPost from './MainFeaturedPost';
import MainLayout from '../../modules/MainLayout'

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
        <MainLayout>
          <MainFeaturedPost mainFeaturedPost={mainFeaturedPost} />
        </MainLayout>
      </Container>
    </Fragment>
  );
}
