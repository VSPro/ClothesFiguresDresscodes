import { makeStyles } from '@material-ui/core/styles';

export const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  mainContainerContent: {},
  imgClass: {},
  mainTitle: {},
  buttons: {
    '& > *': {
      margin: theme.spacing(4),
    },
  },
}));
