import numpy as np
import streamlit as st
import pandas as pd
import altair as alt

def compute(initial_wealth,faster_growth,slower_growth,p_faster_growth):
    total_in=1000
    time_step=60
    df_dict={}
    df_dict['Time_step']=np.arange(61)

    for i in range(total_in):
        samples=np.random.binomial(1,(p_faster_growth),time_step)
        result=[]
        result.append(initial_wealth)
        current_wealth=initial_wealth

        for j in range(time_step):

            if samples[j]:
                current_wealth=current_wealth*(1+(faster_growth/100))
            else:
                current_wealth=current_wealth*(1+slower_growth/100)

            result.append(current_wealth) 
            
        df_dict["Individual"+str(i+1)]=result
    df=pd.DataFrame(df_dict)
    # st.write(df)
    ensemble(df)
     
def ensemble(df):
    #Ensemble Average

    st.header("Ensemble Average")
    average=[]
    for i in range(61):
        average.append(sum(df.loc[i])/1000)
    ensemble_df=pd.DataFrame({"Ensemble_avg":average,"TimeStep":list(np.arange(61))})
    st.altair_chart(alt.Chart(ensemble_df).mark_line().encode(x="TimeStep",
                                                            y="Ensemble_avg"),
                                                            use_container_width=False)

    # End Wealth Distribution
    st.header('End Wealth Distribution')
    end_dis_df=pd.DataFrame({"timestep60":df.loc[60]})

    hist=(alt.Chart(end_dis_df).transform_joinaggregate(
        frequency='count(*)').transform_calculate(
            percentage='1/datum.frequency').mark_bar().encode(
            x=alt.X("timestep60:Q",
            bin=alt.Bin(step=(end_dis_df['timestep60'].max()- end_dis_df['timestep60'].min())/10),
            title="End Wealth(Mean markd in red)"),
            y=alt.Y('sum(percentage):Q',
            axis=alt.Axis(format='%'),
            title='Percentage of Total Individuals')))

    rule=(alt.Chart(end_dis_df).mark_rule(color='red').encode(
                x="mean(timestep60):Q",size=alt.value(2)))
    st.altair_chart(hist+rule)
    wealth_distribution_progression(df)

def wealth_distribution_progression(df):
    st.header('Wealth Distribution Progression')

    long_df=pd.melt(df,id_vars=['Time_step'],var_name='Individuals',value_name='Wealth')
    # st.write(long_df)
    st.altair_chart(alt.Chart(long_df).mark_line().encode(
                    x=alt.X('Time_step',title='Progression of time'),
                    y=alt.Y('Wealth',title='wealth'),
                    color=alt.Color('Individuals',legend=None)
    ))
    




if __name__=='__main__':
    # compute(1000,20,2,0.05)
    st.title("Wealth Progression Experiment")
    st.header("Experiment Parameters")

    initial_wealth=st.sidebar.slider("Intial Wealth",1000,1000000,1000)
    faster_growth=st.sidebar.slider("Faster Growth %",0,100,20)
    slower_growth=st.sidebar.slider("Slower Growth %",-100,100,2)
    p_faster_growth=st.sidebar.slider("Probability of Faster Growth ",0.0,1.0,0.05)

    st.write(f"""
    *Number of Individuals =1000 \n
    *Time Step=60\n
    *Initial Wealth=${initial_wealth}\n
    *Faster Growth={faster_growth}%\n
    *Slower Growth={slower_growth}%\n
    *Probability of Faster Growth={p_faster_growth}\n
    """)
    st.write('Experiment Completed ! Rendering Visualization')

    if st.sidebar.button("Run Experiment"):
        compute(initial_wealth,faster_growth,slower_growth,p_faster_growth)