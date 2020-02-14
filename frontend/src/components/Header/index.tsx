import React from 'react';
import { withRouter } from "react-router-dom";
import { Toolbar } from '@material-ui/core';
import Link from '@material-ui/core/Link';
import { useStyles } from './style'

interface Section {
  title: string;
  url: string;
  img?: string;
}

interface Props {
  history: any,
}

const sections = [
  { title: 'О СЕРВИСЕ', url: '/' },
  { title: 'ОЦЕНКА ФИГУРЫ', url: '/' },
  { title: 'КАК СНИМАТЬ МЕРКИ', url: '/' },
  { title: 'ТИРЫ ФИГУР', url: '/' },
  { title: 'ПОДБОР ОДЕЖДЫ', url: '/' },
  { title: 'bucket', url: '/', img: '' },
];

const Header: React.FC<Props> = ({
  history,
}) => {
  const { toolBarSecondary, toolBarLink, toolBarLabel } = useStyles();

  return (
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
          onClick={ () => {
            history.push(section.url)
          }}
        >
          {section.title}
        </Link>
      ))}
    </Toolbar>
  );
}

export default withRouter(Header)
