import pandas as pd
import numpy as np
import datetime as dt
from datetime import date
from datetime import timedelta
import os
import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

def seasonals_chart(tick):
	ticker=tick
	cycle_start=1951
	cycle_label='Third Year of Cycle'
	cycle_var='pre_election'
	adjust=0
	plot_ytd="Yes"
	all_=""
	end_date=dt.datetime(2022,12,30)

	spx1=yf.Ticker(ticker)
	spx = spx1.history(period="max",end=end_date)
	spx["log_return"] = np.log(spx["Close"] / spx["Close"].shift(1))*100

	spx["day_of_month"] = spx.index.day
	spx['day_of_year'] = spx.index.day_of_year
	spx['month'] = spx.index.month
	spx['Fwd_5dR']=spx.log_return.shift(-5).rolling(window=5).sum().round(2)
	spx['Fwd_10dR']=spx.log_return.shift(-10).rolling(window=10).sum().round(2)
	spx['Fwd_21dR']=spx.log_return.shift(-21).rolling(window=21).sum().round(2)
	spx["year"] = spx.index.year

	#second dataframe explicity to count the number of trading days so far this year
	now = dt.datetime.now()
	days = yf.download(ticker, start="2022-12-31", end=now)
	days["log_return"] = np.log(days["Close"] / days["Close"].shift(1))*100
	days['day_of_year'] = days.index.day_of_year
	days['this_yr']=days.log_return.cumsum()
	days2=days.reset_index(drop=True)
	length=len(days)+adjust


	#create your list of all years
	start=spx['year'].min()
	stop=spx['year'].max()
	r=range(0,(stop-start+1),1)
	print(start)
	years=[]
	for i in r:
		j=start+i
		years.append(j)
	# print(years)


	def yearly(time):
			rslt_df2 = spx.loc[spx['year']==time] 
			grouped_by_day = rslt_df2.groupby("day_of_year").log_return.mean()
			day_by_day=[]
			for day in grouped_by_day:
				cum_return = day
				day_by_day.append(cum_return)
			return day_by_day

	def yearly_5d(time):
		rslt_df2 = spx.loc[spx['year']==time]
		fwd_5_by_day=rslt_df2.groupby("day_of_year").Fwd_5dR.mean()
		day_by_day_5=[]
		for day in fwd_5_by_day:
			cum_return = day
			day_by_day_5.append(cum_return)
		return day_by_day_5

	def yearly_10d(time):
		rslt_df2 = spx.loc[spx['year']==time]
		fwd_5_by_day=rslt_df2.groupby("day_of_year").Fwd_10dR.mean()
		day_by_day_5=[]
		for day in fwd_5_by_day:
			cum_return = day
			day_by_day_5.append(cum_return)
		return day_by_day_5

	def yearly_21d(time):
		rslt_df2 = spx.loc[spx['year']==time]
		fwd_5_by_day=rslt_df2.groupby("day_of_year").Fwd_21dR.mean()
		day_by_day_5=[]
		for day in fwd_5_by_day:
			cum_return = day
			day_by_day_5.append(cum_return)
		return day_by_day_5


	yr_master=[]
	for year in years:
		yearly(year)
		yr_master.append(yearly(year))

	#create list of years corresponding to specific year within 4 year presidential cycle
	l=range(0,19,1)
	years_mid=[]
	for i in l:
		j=cycle_start+i*4
		years_mid.append(j)
	print(years_mid)
	years_mid2=[]
	for i in l:
		j=cycle_start+1+(i*4)
		years_mid2.append(j)

	years_mid3=[]
	for i in l:
		j=cycle_start+2+(i*4)
		years_mid3.append(j)

	years_mid4=[]
	for i in l:
		j=cycle_start-1+(i*4)
		years_mid4.append(j)

	###cycle years start w/ whatever the current year of the cycle is and then move forward from there. EG if it is 2019 then 1. would be pre_election 2. would be election etc.

	###create your empty lists to add your [1d] returns for each year of the cycle.
	yr_mid_master=[]
	yr_mid_master2=[]
	yr_mid_master3=[]
	yr_mid_master4=[]

	###run the one day forward returns function on each set of cycle years to get 4 sets of returns. 
	###Once this for loop is done you'll be left with 4 lists of daily returns for each year that you had in the list
	for year in years_mid:
		yearly(year)
		yr_mid_master.append(yearly(year))
	for year in years_mid2:
		yearly(year)
		yr_mid_master2.append(yearly(year))
	for year in years_mid3:
		yearly(year)
		yr_mid_master3.append(yearly(year))
	for year in years_mid4:
		yearly(year)
		yr_mid_master4.append(yearly(year))

	yr_master2=[]
	for year in years:
		yearly_5d(year)
		yr_master2.append(yearly_5d(year))

	yr_master_mid2=[]
	yr_master_mid22=[]
	yr_master_mid23=[]
	yr_master_mid24=[]
	for year in years_mid:
		yearly_5d(year)
		yr_master_mid2.append(yearly_5d(year))
	for year in years_mid2:
		yearly_5d(year)
		yr_master_mid22.append(yearly_5d(year))
	for year in years_mid3:
		yearly_5d(year)
		yr_master_mid23.append(yearly_5d(year))
	for year in years_mid4:
		yearly_5d(year)
		yr_master_mid24.append(yearly_5d(year))

	yr_master3=[]
	for year in years:
		yearly_10d(year)
		yr_master3.append(yearly_10d(year))

	yr_master_mid3=[]
	yr_master_mid32=[]
	yr_master_mid33=[]
	yr_master_mid34=[]
	for year in years_mid:
		yearly_10d(year)
		yr_master_mid3.append(yearly_10d(year))
	for year in years_mid2:
		yearly_10d(year)
		yr_master_mid32.append(yearly_10d(year))
	for year in years_mid3:
		yearly_10d(year)
		yr_master_mid33.append(yearly_10d(year))
	for year in years_mid4:
		yearly_10d(year)
		yr_master_mid34.append(yearly_10d(year))

	yr_master4=[]
	for year in years:
		yearly_21d(year)
		yr_master4.append(yearly_21d(year))

	yr_master_mid4=[]
	yr_master_mid42=[]
	yr_master_mid43=[]
	yr_master_mid44=[]
	for year in years_mid:
		yearly_21d(year)
		yr_master_mid4.append(yearly_21d(year))
	for year in years_mid2:
		yearly_21d(year)
		yr_master_mid42.append(yearly_21d(year))
	for year in years_mid3:
		yearly_21d(year)
		yr_master_mid43.append(yearly_21d(year))
	for year in years_mid4:
		yearly_21d(year)
		yr_master_mid44.append(yearly_21d(year))

	###you are now converting your lists of returns into dataframes, and then manipulating the resulting data to get averages across all years from the same day.
	###this process is repeated for each cycle year, and for 5d 10d and 21d forward returns. 
	df_all_5d=pd.DataFrame(yr_master2).round(3)
	df_all_5d_mean=df_all_5d.mean().round(2)
	df_all_5d_median=df_all_5d.median().round(2)
	rank=df_all_5d.rank(pct=True).round(3)*100

	df_mt_5d=pd.DataFrame(yr_master_mid2).round(3)
	df_mt_5d_mean=df_mt_5d.mean().round(2)
	df_mt_5d_median=df_mt_5d.median().round(2)
	rank2=df_mt_5d.rank(pct=True).round(3)*100

	df_mt2_5d=pd.DataFrame(yr_master_mid22).round(3)
	df_mt2_5d_mean=df_mt2_5d.mean().round(2)
	rank22=df_mt2_5d.rank(pct=True).round(3)*100

	df_mt3_5d=pd.DataFrame(yr_master_mid23).round(3)
	df_mt3_5d_mean=df_mt3_5d.mean().round(2)
	rank23=df_mt3_5d.rank(pct=True).round(3)*100

	df_mt4_5d=pd.DataFrame(yr_master_mid24).round(3)
	df_mt4_5d_mean=df_mt4_5d.mean().round(2)
	rank24=df_mt4_5d.rank(pct=True).round(3)*100

	df_all_10d=pd.DataFrame(yr_master3).round(3)
	df_all_10d_mean=df_all_10d.mean().round(2)
	df_all_10d_median=df_all_10d.median().round(2)
	rank3=df_all_10d.rank(pct=True).round(3)*100

	df_mt_10d=pd.DataFrame(yr_master_mid3).round(3)
	df_mt_10d_mean=df_mt_10d.mean().round(2)
	df_mt_10d_median=df_mt_10d.median().round(2)
	rank4=df_mt_10d.rank(pct=True).round(3)*100

	df_mt2_10d=pd.DataFrame(yr_master_mid32).round(3)
	df_mt2_10d_mean=df_mt2_10d.mean().round(2)
	rank42=df_mt2_10d.rank(pct=True).round(3)*100

	df_mt3_10d=pd.DataFrame(yr_master_mid33).round(3)
	df_mt3_10d_mean=df_mt3_10d.mean().round(2)
	rank43=df_mt3_10d.rank(pct=True).round(3)*100

	df_mt4_10d=pd.DataFrame(yr_master_mid34).round(3)
	df_mt4_10d_mean=df_mt4_10d.mean().round(2)
	rank44=df_mt4_10d.rank(pct=True).round(3)*100

	df_all_21d=pd.DataFrame(yr_master4).round(3)
	df_all_21d_mean=df_all_21d.mean().round(2)
	df_all_21d_median=df_all_21d.median().round(2)
	rank5=df_all_21d_mean.rank(pct=True).round(3)*100

	df_mt_21d=pd.DataFrame(yr_master_mid4).round(3)
	df_mt_21d_mean=df_mt_21d.mean().round(2)
	df_mt_21d_median=df_mt_21d.median().round(2)
	rank6=df_mt_21d_mean.rank(pct=True).round(3)*100

	df_mt2_21d=pd.DataFrame(yr_master_mid42).round(3)
	df_mt2_21d_mean=df_mt2_21d.mean().round(2)
	rank62=df_mt2_21d_mean.rank(pct=True).round(3)*100

	df_mt3_21d=pd.DataFrame(yr_master_mid43).round(3)
	df_mt3_21d_mean=df_mt3_21d.mean().round(2)
	rank63=df_mt3_21d_mean.rank(pct=True).round(3)*100

	df_mt4_21d=pd.DataFrame(yr_master_mid44).round(3)
	df_mt4_21d_mean=df_mt4_21d.mean().round(2)
	rank64=df_mt4_21d_mean.rank(pct=True).round(3)*100

	pre_election=[]
	election=[]
	post_election=[]
	midterms=[]

	pre_election_list=[df_mt_5d_mean,df_mt_10d_mean,df_mt_21d_mean]
	election_list=[df_mt2_5d_mean,df_mt2_10d_mean,df_mt2_21d_mean]
	post_election_list=[df_mt3_5d_mean,df_mt3_10d_mean,df_mt3_21d_mean]
	midterms_list=[df_mt4_5d_mean,df_mt4_10d_mean,df_mt4_21d_mean]

	for g in pre_election_list:
		pre_election.append(g)
	pre_election_df=pd.DataFrame(pre_election).transpose().rename(columns={0:'Fwd_R5',1:'Fwd_R10',2:'Fwd_R21',})
	pre_election_df['avg']=pre_election_df.mean(axis=1).round(2)

	for g in election_list:
		election.append(g)
	election_df=pd.DataFrame(election).transpose().rename(columns={0:'Fwd_R5',1:'Fwd_R10',2:'Fwd_R21',})
	election_df['avg']=election_df.mean(axis=1).round(2)

	for g in post_election_list:
		post_election.append(g)
	post_election_df=pd.DataFrame(post_election).transpose().rename(columns={0:'Fwd_R5',1:'Fwd_R10',2:'Fwd_R21',})
	post_election_df['avg']=post_election_df.mean(axis=1).round(2)

	for g in midterms_list:
		midterms.append(g)
	midterms_df=pd.DataFrame(midterms).transpose().rename(columns={0:'Fwd_R5',1:'Fwd_R10',2:'Fwd_R21',})
	midterms_df['avg']=midterms_df.mean(axis=1).round(2)

	cycles_df=pd.concat([pre_election_df['avg'],election_df['avg'],post_election_df['avg'],midterms_df['avg']],axis=1,keys=['pre_election','election','post_election','midterms'])
	cycles_df=cycles_df.stack().reset_index()
	cycles_df.columns.values[2]="avg"
	cycles_df.columns.values[1]=ticker
	cycles_df['rnk']=cycles_df.avg.rank(pct=True).round(3)*100


	print_df1=cycles_df[cycles_df[ticker] == cycle_var].reset_index(drop=True)
	trailing_cycle=print_df1.iloc[length-5:length].rnk.mean()
	print_df=print_df1[print_df1['level_0'] == length]
	print_df=print_df.reset_index(drop=True)
	true_cycle_rnk=print_df['rnk'].iat[-1].round(1)


	returns=[]
	tuples=[df_all_5d_mean,df_mt_5d_mean,df_all_10d_mean,df_mt_10d_mean,df_all_21d_mean,df_mt_21d_mean]
	for data in tuples:
		returns.append(data)
	new_df=pd.DataFrame(returns).transpose().rename(columns={
															0:'Fwd_R5',1:'Fwd_R5_MT',
															2:'Fwd_R10',3:'Fwd_R10_MT',
															4:'Fwd_R21',5:'Fwd_R21_MT',																						
	})

	#5d stuff

	new_df['Returns_5_rnk']=new_df.Fwd_R5.rank(pct=True).round(3)*100
	new_df['Returns_5_rnk_mt']=new_df.Fwd_R5_MT.rank(pct=True).round(3)*100

	r_5=new_df['Fwd_R5'][[length]].round(2)
	r_5_mt=new_df['Fwd_R5_MT'][[length]].round(2)
	r_5_ptile=new_df['Returns_5_rnk'][[length]].round(2)
	r_5_ptile_mt=new_df['Returns_5_rnk_mt'][[length]].round(2)

	#10d stuff

	new_df['Returns_10_rnk']=new_df.Fwd_R10.rank(pct=True).round(3)*100
	new_df['Returns_10_rnk_mt']=new_df.Fwd_R10_MT.rank(pct=True).round(3)*100

	r_10=new_df['Fwd_R10'][[length]].round(2)
	r_10_mt=new_df['Fwd_R10_MT'][[length]].round(2)
	r_10_ptile=new_df['Returns_10_rnk'][[length]].round(2)
	r_10_ptile_mt=new_df['Returns_10_rnk_mt'][[length]].round(2)

	#21d stuff
	new_df['Returns_21_rnk']=new_df.Fwd_R21.rank(pct=True).round(3)*100
	new_df['Returns_21_rnk_mt']=new_df.Fwd_R21_MT.rank(pct=True).round(3)*100

	##Calculate average ranks across the row
	new_df['Returns_all_avg']=new_df[['Returns_21_rnk','Returns_10_rnk','Returns_5_rnk']].mean(axis=1)
	new_df['Returns_all_avg_mt']=new_df[['Returns_21_rnk_mt','Returns_10_rnk_mt','Returns_5_rnk_mt']].mean(axis=1)
	new_df['Returns_all_avg_10dt']=new_df['Returns_all_avg'].rolling(window=10).mean().shift(1)
	new_df['Returns_all_avg_mt_10dt']=new_df['Returns_all_avg_mt'].rolling(window=10).mean().shift(1)
	new_df['Seasonal_delta']=new_df.Returns_all_avg - new_df.Returns_all_avg_10dt
	new_df['Seasonal_delta_cycle']=new_df.Returns_all_avg_mt - new_df.Returns_all_avg_mt_10dt


	r_21=new_df['Fwd_R21'][[length]].round(2)
	r_21_mt=new_df['Fwd_R21_MT'][[length]].round(2)
	r_21_ptile=new_df['Returns_21_rnk'][[length]].round(2)
	r_21_ptile_mt=new_df['Returns_21_rnk_mt'][[length]].round(2)


	##Output
	all_5d=r_5_ptile.values[0]
	mt_5d=r_5_ptile_mt.values[0]
	all_10d=r_10_ptile.values[0]
	mt_10d=r_10_ptile_mt.values[0]
	all_21d=r_21_ptile.values[0]
	mt_21d=r_21_ptile_mt.values[0]
	all_avg=((all_5d+all_10d+all_21d)/3).round(2)
	cycle_avg=true_cycle_rnk
	total_avg=((all_avg+true_cycle_rnk)/2).round(2)
	# print(f'''Fwd cycle rank is {true_cycle_rnk}
	# Fwd cycle delta is {abs(true_cycle_rnk-trailing_cycle).round(2)}
	# Fwd all rank is {all_avg}
	# Fwd Avg rank is {total_avg}
	# ''')


	if ticker == '^GSPC':
		ticker2 = 'SPX'
	else:
		ticker2 = ticker

	length= len(days) + adjust
	c=days.Close[-1]

	dfm=pd.DataFrame(yr_mid_master)
	dfm1=dfm.mean()
	s4=dfm1.cumsum()


	dfy=pd.DataFrame(yr_master)
	dfy1=dfy.mean()
	s3=dfy1.cumsum()
	##Mean Return paths chart (looks like a classic 'seasonality' chart)
	# plot2=plt.figure(2)
	fig = go.Figure()

	fig.add_trace(go.Scatter(x=s4.index, y=s4.values, mode='lines', name=cycle_label, line=dict(color='orange')))
	if plot_ytd == 'Yes':
	    fig.add_trace(go.Scatter(x=days2.index, y=days2['this_yr'], mode='lines', name='Year to Date', line=dict(color='green')))

	y1 = max(s4.max(), days2['this_yr'].max()) if plot_ytd == 'Yes' else s4.max()
	y0=min(s4.min(),days2['this_yr'].min(),0)
	# Assuming 'length' variable is defined and within the range of the x-axis
	length_value = length

	# Interpolate Y value at the specified X coordinate
	y_value_at_length = np.interp(length_value, s4.index, s4.values)
	y_2_value_at_length = np.interp(length_value, s3.index, s3.values)

	# Add a white dot at the specified X coordinate and the interpolated Y value
	fig.add_trace(go.Scatter(x=[length_value], y=[y_value_at_length], mode='markers', marker=dict(color='white', size=6), name='White Dot' ,showlegend=False))
# 	fig.add_trace(go.Scatter(x=s3.index, y=s3.values, mode='lines', name='Mean Return', line=dict(color='blue')))
	fig.add_trace(go.Scatter(x=[length_value], y=[y_2_value_at_length], mode='markers', marker=dict(color='white', size=6), name='White Dot' ,showlegend=False))
	
	fig.update_layout(
	    title=f"Mean return path for {ticker2} in years {start}-present",
	    legend=dict(
	        bgcolor='rgba(0,0,0,0)',
	        font=dict(color='White'),
	        itemclick='toggleothers',
	        itemdoubleclick='toggle',
	        traceorder='reversed',
	        orientation='h',
	        bordercolor='grey',
	        borderwidth=1,
	    ),
	    xaxis=dict(title='Date', color='white',showgrid=False),
	    yaxis=dict(title='Mean Return', color='white',showgrid=False),
	    font=dict(color='white'),
	    margin=dict(l=40, r=40, t=40, b=40),
	    hovermode='x',
	    plot_bgcolor='Black',
	    paper_bgcolor='Black'
	)

	st.plotly_chart(fig)

megas_list=['ETH-USD','BTC-USD','^GSPC','^IXIC','^RUT','^RUO','SLV','GLD']
for stock in megas_list:
	seasonals_chart(stock)
