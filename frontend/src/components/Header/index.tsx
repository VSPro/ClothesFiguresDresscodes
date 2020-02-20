import React from 'react';
import { withRouter, RouteComponentProps } from 'react-router-dom';
import { Toolbar } from '@material-ui/core';
import Link from '@material-ui/core/Link';
import { useStyles } from './styles';

interface HeaderItem {
  pageUrl: string;
  pageTitle: string;
}
interface Props {
  history: any;
  headerItems?: HeaderItem[];
}

const Header: React.FC<Props & RouteComponentProps<any>> = ({ history, headerItems }) => {
  const { toolBarSecondary, toolBarLink, toolBarLabel } = useStyles();

  return (
    <Toolbar component="nav" className={toolBarSecondary} variant="regular">
      <Link color="primary" noWrap key={'Main'} variant="body2" href="#" className={toolBarLabel}>
        НаСтиле
      </Link>
      {headerItems?.map((headerItem: HeaderItem) => (
        <Link
          color="primary"
          noWrap
          key={headerItem.pageTitle}
          variant="body2"
          className={toolBarLink}
          onClick={() => {
            history.push(headerItem.pageUrl);
          }}
        >
          {headerItem.pageTitle}
        </Link>
      ))}
    </Toolbar>
  );
};

export default withRouter(Header);
