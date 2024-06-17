## ===================================================================== ##
## function definitions
##

## prediction with user-specified cov-matrix
predict.fixest <- function(model_fixest, newdata){
  m.mat <- as.matrix(newdata)
  m.coef <- coef(model_fixest)
  vcov <- vcov(model_fixest)
  m.coef <- m.coef[labels(m.coef)[[1]] %in% labels(m.mat)[[2]]]
  m.vcov <- vcov[labels(vcov)[[1]] %in% labels(m.mat)[[2]], labels(vcov)[[2]] %in% labels(m.mat)[[2]]]
  fit <- as.vector(m.mat %*% m.coef)
  se.fit <- sqrt(diag(m.mat%*%m.vcov%*%t(m.mat)))
  return(list(fit=fit, se.fit=se.fit))
}

## ============================================================================================================================================
## data preparation
##

library(fixest)
library(splines)

## =======================

DATAPATH <- '/media/manuel/manuel-external2/project_32/data_final/'

## =======================

print('Reading data...')

df <- read.csv(paste0(DATAPATH, "data_demeaned.csv"))
df <- df[complete.cases(df[, c('dependent', 'a1', 'tp_mean', 't2m_mean')]), ]

## ================================================================================================================
## POOLED estimation
## ================================================================================================================

if (TRUE) { # START IF

	print('Estimating pooled model...')
	model_fixest <- feols(dependent ~ +0 + a1 + a2 + a3 + a4 + a5 + a6 + tp_mean + tp_mean_dummy, df, vcov='hc1')
	meanvalue <- mean(df$t2m_mean)
	splinebasisnames <- paste0('a', 1:6)
	predvars <- c(splinebasisnames, 'tp_mean', 'tp_mean_dummy')
	coords <- c(seq(min(df$t2m_mean), max(df$t2m_mean), by=0.1), meanvalue)
	newdata <- data.frame(list(t2m_mean=coords))
	knots <- quantile(df$t2m_mean, c(0.25, 0.5, 0.75))
	bsmat <- bs(newdata$t2m_mean, knots=knots, degree=3) # knots = df - degree
	newdata[, splinebasisnames] <- bsmat
	newdata <- newdata - newdata[rep(nrow(newdata), nrow(newdata)), ]
	newdata <- newdata[1:(nrow(newdata)-1), ]
	newdata$tp_mean <- 0.
	newdata$tp_mean_dummy <- 0.
	newdataX <- newdata[, predvars]
	pred <- data.frame(predict.fixest(model_fixest, newdataX))
	pred$t2m_mean <- newdata$t2m_mean + meanvalue
	write.csv(pred, paste0('./results/predictions_byunit_01a_', 'POOLED', '.csv'))

} # END IF

## ================================================================================================================
## BY UNIT estimations
## ================================================================================================================
## by unit, splines

if (TRUE) { # START IF

for (unit in unique(df$id)) {

	print(unit)

	dfi <- df[df$id == unit, ]

	model_fixest <- feols(dependent ~ +0 + b1 + b2 + b3 + b4 + b5 + b6 + tp_mean + tp_mean_dummy, dfi, vcov='hc1')

	if (length(coef(model_fixest)) > 6) {

	meanvalue <- mean(dfi$t2m_mean)
	splinebasisnames <- paste0('b', 1:6)
	predvars <- c(splinebasisnames, 'tp_mean', 'tp_mean_dummy')
	coords <- c(seq(min(dfi$t2m_mean), max(dfi$t2m_mean), by=0.1), meanvalue)
	newdata <- data.frame(list(t2m_mean=coords))
  knots <- quantile(dfi$t2m_mean, c(0.25, 0.5, 0.75))
	bsmat <- bs(newdata$t2m_mean, knots=knots, degree=3) # knots = df - degree
	newdata[, splinebasisnames] <- bsmat
	newdata <- newdata - newdata[rep(nrow(newdata), nrow(newdata)), ]
	newdata <- newdata[1:(nrow(newdata)-1), ]
	newdata$tp_mean <- 0.
	newdata$tp_mean_dummy <- 0.
	newdataX <- newdata[, predvars]
	pred <- data.frame(predict.fixest(model_fixest, newdataX))
	pred$t2m_mean <- newdata$t2m_mean + meanvalue
	write.csv(pred, paste0('./results/predictions_byunit_01a_', unit, '.csv'))

	} else {
		print(paste0('Collinearity, unit: ', unit))
	}

}
} # END IF

## ============================================================================================================================================
## splines with two knots

if (TRUE) {

for (unit in unique(df$id)) {

	print(unit)

	dfi <- df[df$id == unit, ]

	model_fixest <- feols(dependent ~ +0 + c1 + c2 + c3 + c4 + c5 + tp_mean + tp_mean_dummy, dfi, vcov='hc1')

	if (length(coef(model_fixest)) > 5) {

	meanvalue <- mean(dfi$t2m_mean)
	splinebasisnames <- paste0('c', 1:5)
	predvars <- c(splinebasisnames, 'tp_mean', 'tp_mean_dummy')
	coords <- c(seq(min(dfi$t2m_mean), max(dfi$t2m_mean), by=0.1), meanvalue)
	newdata <- data.frame(list(t2m_mean=coords))
  knots <- quantile(dfi$t2m_mean, c(0.33, 0.66))
	bsmat <- bs(newdata$t2m_mean, knots=knots, degree=3) # knots = df - degree
	newdata[, splinebasisnames] <- bsmat
	newdata <- newdata - newdata[rep(nrow(newdata), nrow(newdata)), ]
	newdata <- newdata[1:(nrow(newdata)-1), ]
	newdata$tp_mean <- 0.
	newdata$tp_mean_dummy <- 0.
	newdataX <- newdata[, predvars]
	pred <- data.frame(predict.fixest(model_fixest, newdataX))
	pred$t2m_mean <- newdata$t2m_mean + meanvalue
	write.csv(pred, paste0('./results/predictions_byunit_01b_', unit, '.csv'))

	} else {
		print(paste0('Collinearity, unit: ', unit))
	}

}
} # END IF

## ============================================================================================================================================
## rainfall splines

if (TRUE) {

for (unit in unique(df$id)) {

	print(unit)

	dfi <- df[df$id == unit, ]

	model_fixest <- feols(dependent ~ +0 + b1 + b2 + b3 + b4 + b5 + b6 + d1 + d2 + d3 + d4 + d5, dfi, vcov='hc1')

	if (length(coef(model_fixest)) > 10) {

	meanvalue <- mean(dfi$t2m_mean)
	splinebasisnames <- paste0('b', 1:6)
	predvars <- c(splinebasisnames, 'd1', 'd2', 'd3', 'd4', 'd5')
	coords <- c(seq(min(dfi$t2m_mean), max(dfi$t2m_mean), by=0.1), meanvalue)
	newdata <- data.frame(list(t2m_mean=coords))
  knots <- quantile(dfi$t2m_mean, c(0.25, 0.5, 0.75))
	bsmat <- bs(newdata$t2m_mean, knots=knots, degree=3) # knots = df - degree
	newdata[, splinebasisnames] <- bsmat
	newdata <- newdata - newdata[rep(nrow(newdata), nrow(newdata)), ]
	newdata <- newdata[1:(nrow(newdata)-1), ]
	newdata[, c('d1', 'd2', 'd3', 'd4', 'd5')] <- 0.
	newdataX <- newdata[, predvars]
	pred <- data.frame(predict.fixest(model_fixest, newdataX))
	pred$t2m_mean <- newdata$t2m_mean + meanvalue
	write.csv(pred, paste0('./results/predictions_byunit_01c_', unit, '.csv'))

	} else {
		print(paste0('Collinearity, unit: ', unit))
	}

}
} # END IF

## ============================================================================================================================================
## by unit, quantiles

if (TRUE) { # START IF

print('By unit, quantiles...')

for (unit in unique(df$id)) {

	print(unit)

	dfi <- df[df$id == unit, ]
	model_fixest <- feols(dependent ~ q1_1 + q1_2 + q1_3 + q1_4 + q1_5 + q1_7 + q1_8 + q1_9 + q1_10 +
									tp_mean + tp_mean_dummy, dfi, vcov='hc1')
	write.csv(data.frame(model_fixest$coeftable), paste0('./results/coeffs_byunit_02_', unit, '.csv'))

}
} # END IF

## ============================================================================================================================================
## first and second year

if (TRUE) {

for (unit in unique(df$id)) {

	print(unit)

	dfi <- df[df$id == unit, ]
	dfi <- dfi[(dfi$day < 507), ]

	if (nrow(dfi) < 30) {

		print('Not enough obs')

	} else {

	model_fixest <- feols(dependent ~ +0 + b1 + b2 + b3 + b4 + b5 + b6 + tp_mean + tp_mean_dummy, dfi, vcov='hc1')

	if (length(coef(model_fixest)) > 7) {

	meanvalue <- mean(dfi$t2m_mean)
	splinebasisnames <- paste0('b', 1:6)
	predvars <- c(splinebasisnames, 'tp_mean', 'tp_mean_dummy')
	coords <- c(seq(min(dfi$t2m_mean), max(dfi$t2m_mean), by=0.1), meanvalue)
	newdata <- data.frame(list(t2m_mean=coords))
  knots <- quantile(dfi$t2m_mean, c(0.25, 0.5, 0.75))
	bsmat <- bs(newdata$t2m_mean, knots=knots, degree=3) # knots = df - degree
	newdata[, splinebasisnames] <- bsmat
	newdata <- newdata - newdata[rep(nrow(newdata), nrow(newdata)), ]
	newdata <- newdata[1:(nrow(newdata)-1), ]
	newdata$tp_mean <- 0.
	newdata$tp_mean_dummy <- 0.
	newdataX <- newdata[, predvars]
	pred <- data.frame(predict.fixest(model_fixest, newdataX))
	pred$t2m_mean <- newdata$t2m_mean + meanvalue
	write.csv(pred, paste0('./results/predictions_byunit_01Y1_', unit, '.csv'))

	} else {
		print(paste0('Collinearity, unit: ', unit))
	}

	}

}
} # END IF

if (TRUE) { # START IF

for (unit in unique(df$id)) {

	print(unit)

	dfi <- df[df$id == unit, ]
	dfi <- dfi[(dfi$day >= 507), ]

	if (nrow(dfi) < 30) {

		print('Not enough obs')

	} else {

	model_fixest <- feols(dependent ~ +0 + b1 + b2 + b3 + b4 + b5 + b6 + tp_mean + tp_mean_dummy, dfi, vcov='hc1')

	if (length(coef(model_fixest)) > 7) {

	meanvalue <- mean(dfi$t2m_mean)
	splinebasisnames <- paste0('b', 1:6)
	predvars <- c(splinebasisnames, 'tp_mean', 'tp_mean_dummy')
	coords <- c(seq(min(dfi$t2m_mean), max(dfi$t2m_mean), by=0.1), meanvalue)
	newdata <- data.frame(list(t2m_mean=coords))
  knots <- quantile(dfi$t2m_mean, c(0.25, 0.5, 0.75))
	bsmat <- bs(newdata$t2m_mean, knots=knots, degree=3) # knots = df - degree
	newdata[, splinebasisnames] <- bsmat
	newdata <- newdata - newdata[rep(nrow(newdata), nrow(newdata)), ]
	newdata <- newdata[1:(nrow(newdata)-1), ]
	newdata$tp_mean <- 0.
	newdata$tp_mean_dummy <- 0.
	newdataX <- newdata[, predvars]
	pred <- data.frame(predict.fixest(model_fixest, newdataX))
	pred$t2m_mean <- newdata$t2m_mean + meanvalue
	write.csv(pred, paste0('./results/predictions_byunit_01Y2_', unit, '.csv'))

	} else {
		print(paste0('Collinearity, unit: ', unit))
	}

	}

}
} # END IF
