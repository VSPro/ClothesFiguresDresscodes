import React from 'react';
import { withRouter } from "react-router-dom";
import { Toolbar } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Link from '@material-ui/core/Link';

interface Section {
  title: string;
  url: string;
  img?: string;
}

interface Props {
  // sections: Array<Section>;
  history: any,
}

const useStyles = makeStyles(theme => ({
  toolBarSecondary: {
    justifyContent: 'space-between',
    overflowX: 'auto',
  },
  toolBarLabel: {
    flexBasis: 200,
  },

  toolBarLink: {
    padding: theme.spacing(1),
    flexShrink: 0,
  },
}));

/**
 * sections оговариваются в этом компоненте, так как шапка не будет менять своих пунктов
 * при переключении страниц - это логика, которая важна только здесь
 */
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
    //play with variant
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

/**
 * withRouter предоставляет в компонент объекты, завязанные на работу по переключению
 * страниц. Основной объект - это histiry. В нём есть метод push, которому можно указывать 
 * адрес желаемой для перехода страницы
 */
export default withRouter(Header)
