import { makeStyles } from '@material-ui/core/styles';

export const useStyles = makeStyles(theme => ({
  toolBarSecondary: {
    justifyContent: 'space-between',
    overflowX: 'auto',
    paddingTop: '1%',
    paddingRight: '8%',
    paddingLeft: '8%',
    paddingBottom: '1%',
  },
  toolBarLabel: {
    flexBasis: 200,
    '&:hover': {
      textDecoration: 'none',
    },
  },

  toolBarLink: {
    padding: theme.spacing(1),
    flexShrink: 0,
    color: '#0B0A07',
  },
}));
