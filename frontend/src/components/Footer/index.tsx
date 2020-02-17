import React from 'react';
import { withRouter } from 'react-router-dom';
import { Toolbar } from '@material-ui/core';
import Link from '@material-ui/core/Link';
import { useStyles } from './styles';

interface Section {
  title: string;
  url: string;
}

interface Props {
  history: any;
}

const sections = [
  { title: 'О СЕРВИСЕ', url: '/' },
  { title: 'КАК СНИМАТЬ МЕРКИ', url: '/' },
  { title: 'О НОГАХ И ОСАНКЕ', url: '/' },
  { title: 'ПОДБОР ОДЕЖДЫ', url: '/' },
  { title: 'ОЦЕНКА ФИГУРЫ', url: '/' },
  { title: 'ТИРЫ ФИГУР', url: '/' },
  { title: 'СТИЛИ ОДЕЖДЫ', url: '/' },
  { title: 'КОРЗИНА', url: '/' },
];

const Footer: React.FC<Props> = ({ history }) => {
  const { toolBarSecondary, toolBarLink, toolBarLabel, footer } = useStyles();

  return (
    <footer className={footer}>
      <Toolbar component="nav" className={toolBarSecondary} variant="regular">
        <Link color="primary" noWrap key={'Main'} variant="body2" href="#" className={toolBarLabel}>
          НаСтиле
        </Link>
        {sections.map((section: Section) => (
          <Link
            color="primary"
            noWrap
            key={section.title}
            variant="body2"
            className={toolBarLink}
            onClick={() => {
              history.push(section.url);
            }}
          >
            {section.title}
          </Link>
        ))}
      </Toolbar>
    </footer>
  );
};

export default withRouter(Footer);
