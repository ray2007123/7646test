""""""  		  	   		 	   			  		 			     			  	 
"""Assess a betting strategy.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	   			  		 			     			  	 
All Rights Reserved  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	   			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	   			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	   			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   			  		 			     			  	 
or edited.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	   			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	   			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   			  		 			     			  	 
GT honor code violation.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Student Name: Mingming Wang (replace with your name)  		  	   		 	   			  		 			     			  	 
GT User ID: mwang611 (replace with your User ID)  		  	   		 	   			  		 			     			  	 
GT ID: 903561880 (replace with your GT ID)  		  	   		 	   			  		 			     			  	 
"""  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
import numpy as np
import random
import matplotlib.pyplot as plt
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
def author():  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    :return: The GT username of the student  		  	   		 	   			  		 			     			  	 
    :rtype: str  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    return "mwang611"  # replace tb34 with your Georgia Tech username.
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
def gtid():  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    :return: The GT ID of the student  		  	   		 	   			  		 			     			  	 
    :rtype: int  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    return 903561880  # replace with your GT ID number
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
def get_spin_result(win_prob):  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		 	   			  		 			     			  	 
    :type win_prob: float  		  	   		 	   			  		 			     			  	 
    :return: The result of the spin.  		  	   		 	   			  		 			     			  	 
    :rtype: bool  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    result = False  		  	   		 	   			  		 			     			  	 
    if np.random.random() <= win_prob:
        result = True  		  	   		 	   			  		 			     			  	 
    return result  		  	   		 	   			  		 			     			  	 

def bet_exp1(win_prob):
    episode_winnings = 0
    winnings = np.zeros(1000)  # 1000 episodes
    i = 0
    while episode_winnings < 80 and i < 1000:
        won = False
        bet_amount = 1
        while not won:
            won = get_spin_result(win_prob)
            i = i + 1
            if won == True:
                episode_winnings = episode_winnings + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2
            winnings[i] = episode_winnings
    if winnings[i] == 80:
        winnings[i:] = 80
    return winnings

def bet_exp2(win_prob):
    episode_winnings = 0
    winnings = np.zeros(1000)  # 1000 episodes
    bank_roll = 256  # initial bankroll, according to the experiment requirement
    i = 0
    while episode_winnings < 80 and i < 1000 and (episode_winnings + bank_roll) > 0:
        won = False
        bet_amount = min (episode_winnings + bank_roll, 1) # Ensure bet_amount doesn't exceed available funds
        while not won:
            won = get_spin_result(win_prob)
            i = i + 1
            if won == True:
                episode_winnings = episode_winnings + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = min(bet_amount * 2, episode_winnings + bank_roll)
            winnings[i] = episode_winnings
    if episode_winnings >= 80 :
        winnings[i:] = 80
    if episode_winnings + bank_roll <= 0:
        winnings[i:] = np.minimum(winnings[i:], -256)
    return winnings



def test_code():  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    Method to test your code  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    win_prob = 0.4737  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    print(get_spin_result(win_prob))  # test the roulette spin  		  	   		 	   			  		 			     			  	 
    # add your code here to implement the experiments

    # experiment1_figure1
    # Run simple simulator 10 times
    plt.figure(1)
    for i in range(0, 10):
        winnings = bet_exp1(win_prob)
        plt.plot(winnings, label = 'Run %s' % i, color='C%d' % i, linewidth=2)

    plt.xlim((0, 300))
    plt.ylim((-256, 100))
    plt.xlabel('Spin Number', fontsize=12, fontweight='bold')
    plt.ylabel('Winnings Number', fontsize=12, fontweight='bold')
    plt.legend()
    plt.grid(True,  which='both', linestyle='--', linewidth=0.5)  # 启用网格
    plt.title("Figure 1: Monte Carlo simulation for 10 times", fontsize=14, fontweight='bold')
    # 设置边框属性
    for spine in plt.gca().spines.values():
        spine.set_linewidth(2)  # 设置边框宽度为2
    plt.savefig('1.png')
    plt.close()

    # experiment1_figure2
    # Run simple simulator 1000 times
    winningsTotal = np.zeros((1000, 1000))

    for i in range(1000):
        winningsTotal[i, :] = bet_exp1(win_prob)

    mean_winnings = np.mean(winningsTotal, axis=0)
    std_winnings = np.std(winningsTotal, axis=0)
    upper_line = mean_winnings + std_winnings
    lower_line = mean_winnings - std_winnings

    plt.figure(2)
    plt.plot(mean_winnings, label="Mean", color='C0', linewidth=1.5)
    plt.plot(upper_line, label="Mean + Standard Deviation", color='C1', linewidth=1.5, linestyle='--')
    plt.plot(lower_line, label="Mean - Standard Deviation", color='C2', linewidth=1.5, linestyle='--')

    plt.xlim((0, 300))
    plt.ylim((-256, 100))
    plt.xlabel('Spin Number', fontsize=12, fontweight='bold')
    plt.ylabel('Winnings Number', fontsize=12, fontweight='bold')
    plt.legend()
    plt.title("Figure 2: mean of winnings after 1000 times simulation", fontsize=14, fontweight='bold')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # Set border properties
    for spine in plt.gca().spines.values():
        spine.set_linewidth(2)  # Set border width to 2
    plt.savefig('2.png')
    plt.close()

    # experiment1_figure3
    # Run simple simulator 1000 times and plot median instead of mean
    median_winnings = np.median(winningsTotal, axis=0)
    upper_line = median_winnings + std_winnings
    lower_line = median_winnings - std_winnings

    plt.figure(3)
    plt.plot(mean_winnings, label="Median", color='C0', linewidth=1.5)
    plt.plot(upper_line, label="Median + Standard Deviation", color='C1', linewidth=1.5, linestyle='--')
    plt.plot(lower_line, label="Median - Standard Deviation", color='C2', linewidth=1.5, linestyle='--')

    plt.xlim((0, 300))
    plt.ylim((-256, 100))
    # Set x and y axis label fonts
    plt.xlabel('Spin Number', fontsize=12, fontweight='bold')
    plt.ylabel('Winnings Number', fontsize=12, fontweight='bold')

    plt.legend()
    plt.title("Figure 3: median of winnings after 1000 times simulation", fontsize=13, fontweight='bold')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Set border properties
    for spine in plt.gca().spines.values():
        spine.set_linewidth(2)  # Set border width to 2
    plt.savefig('3.png')
    plt.close()

    # experiment2_figure4
    # Run 1000 times
    winningsTotal2 = np.zeros((1000, 1000))
    for i in range(1000):
        winningsTotal2[i, :] = bet_exp2(win_prob)

    mean_winnings = np.mean(winningsTotal2, axis=0)
    std_winnings = np.std(winningsTotal2, axis=0)
    upper_line = mean_winnings + std_winnings
    lower_line = mean_winnings - std_winnings

    plt.figure(4)
    plt.plot(mean_winnings, label="Mean", color='C0', linewidth=1.5)
    plt.plot(upper_line, label="Mean + Standard Deviation", color='C1', linewidth=1.5, linestyle='--')
    plt.plot(lower_line, label="Mean - Standard Deviation", color='C2', linewidth=1.5, linestyle='--')

    plt.xlim((0, 300))
    plt.ylim((-256, 100))
    plt.xlabel('Spin Number', fontsize=12, fontweight='bold')
    plt.ylabel('Winnings Number', fontsize=12, fontweight='bold')
    plt.legend()
    plt.title("Figure 4: mean of winnings after 1000 times limited simulation", fontsize=12, fontweight='bold')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # Set border properties
    for spine in plt.gca().spines.values():
        spine.set_linewidth(2)  # Set border width to 2

    plt.savefig('4.png')
    plt.close()

    # experiment2_figure5
    # Run 1000 times
    median_winnings = np.median(winningsTotal2, axis=0)

    upper_line = median_winnings + std_winnings
    lower_line = median_winnings - std_winnings

    plt.figure(5)
    plt.plot(median_winnings, label="Median", color='C0', linewidth=1.5)
    plt.plot(upper_line, label="Median + Standard Deviation", color='C1', linewidth=1.5, linestyle='--')
    plt.plot(lower_line, label="Median - Standard Deviation", color='C2', linewidth=1.5, linestyle='--')

    plt.xlim((0, 300))
    plt.ylim((-256, 100))
    plt.xlabel('Spin Number', fontsize=12, fontweight='bold')
    plt.ylabel('Winnings Number', fontsize=12, fontweight='bold')
    plt.legend()
    plt.title("Figure 5: median of winnings after 1000 times limited simulation", fontsize=12, fontweight='bold')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # Set border properties
    for spine in plt.gca().spines.values():
        spine.set_linewidth(2)  # Set border width to 2

    plt.savefig('5.png')
    plt.close()

if __name__ == "__main__":  		  	   		 	   			  		 			     			  	 
    test_code()  		  	   		 	   			  		 			     			  	 
