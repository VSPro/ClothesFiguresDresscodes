import FirstPage from './pages/AboutPage/FirstPage';
import FigureCalculationPage from './pages/FigureCalculationPage';
import FiltersPage from './pages/FiltersPage';
import NotFoundPage from './pages/NotFoundPage';
import FrontPage from './pages/FrontPage/';

import { PageConfig } from './modules/MainLayout';

const urlScheme: PageConfig[] = [
    {
      pageTitle: 'О сервисе',
      pageUrl: '/',
      component: FrontPage,
    },
    {
      pageTitle: 'Оценка фигуры',
      pageUrl: '/type-of-figure-calculation',
      component: FigureCalculationPage,
    }
  ]

export default urlScheme
