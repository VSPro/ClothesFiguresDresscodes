import React from 'react';
import { Toolbar } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Link from '@material-ui/core/Link';

interface Section {
  title: string;
  url: string;
  img?: string;
}

interface Props {
  sections: Array<Section>;
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

export default function Header({ sections }: Props) {
  const { toolBarSecondary, toolBarLink, toolBarLabel } = useStyles();

  return (
    //play with variant
    <Toolbar component="nav" className={toolBarSecondary} variant="regular">
      <Link color="primary" noWrap key={'Main'} variant="body2" href="#" className={toolBarLabel}>
        НаСтиле
      </Link>
      {sections.map((section: Section) => (
        <Link color="primary" noWrap key={section.title} variant="body2" href={section.url} className={toolBarLink}>
          {section.title}
        </Link>
      ))}
    </Toolbar>
  );
}
