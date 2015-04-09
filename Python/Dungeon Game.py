"""
The demons had captured the princess (P) and imprisoned her in the bottom-right corner of a dungeon. The dungeon consists of M x N rooms laid out in a 2D grid. Our valiant knight (K) was initially positioned in the top-left room and must fight his way through the dungeon to rescue the princess.

The knight has an initial health point represented by a positive integer. If at any point his health point drops to 0 or below, he dies immediately.

Some of the rooms are guarded by demons, so the knight loses health (negative integers) upon entering these rooms; other rooms are either empty (0's) or contain magic orbs that increase the knight's health (positive integers).

In order to reach the princess as quickly as possible, the knight decides to move only rightward or downward in each step.


Write a function to determine the knight's minimum initial health so that he is able to rescue the princess.

For example, given the dungeon below, the initial health of the knight must be at least 7 if he follows the optimal path RIGHT-> RIGHT -> DOWN -> DOWN.

-2 (K)	-3	3
-5	-10	1
10	30	-5 (P)

Notes:

The knight's health has no upper bound.
Any room can contain threats or power-ups, even the first room the knight enters and the bottom-right room where the princess is imprisoned.
"""

class Solution:
    # @param dungeon, a list of lists of integers
    # @return a integer
    def calculateMinimumHP(self, dungeon):
        M = len(dungeon)
        N = len(dungeon[0])
        
        hp = [[0 for _ in xrange(N)] for _ in xrange(M)]
        
        for i in reversed(xrange(M)):
            for j in reversed(xrange(N)):
                if i == M-1 and j == N-1:
                    hp[M-1][N-1] = max(1,1-dungeon[M-1][N-1])
                else:
                    hp[i][j] = max(1,min(float('inf') if j == N-1 else hp[i][j+1],float('inf') if i == M-1 else hp[i+1][j]) \
                    - dungeon[i][j])
        
        return hp[0][0]

# Binary Search
class Solution:
    # @param dungeon, a list of lists of integers
    # @return a integer
    def calculateMinimumHP(self, dungeon):
        maximum_loses = 0
        for rooms in dungeon:
            for room in rooms:
                if room < 0:
                    maximum_loses += abs(room)
                    
        return self.binarySearch(dungeon, maximum_loses)
    
    def binarySearch(self, dungeon, maximum_loses):
        start, end = 1, maximum_loses + 1
        result = 0
        while start < end:
            mid = start + (end - start) / 2
            if self.DP(dungeon, mid):
                end = mid
            else:
                start = mid + 1
        return start
    
    def DP(self, dungeon, HP):
        remain_HP = [0 for _ in dungeon[0]]
        remain_HP[0] = HP + dungeon[0][0]
        for j in xrange(1, len(remain_HP)):
            if remain_HP[j - 1] > 0: 
                remain_HP[j] = max(remain_HP[j - 1] + dungeon[0][j], 0)
                
        for i in xrange(1, len(dungeon)):
            if remain_HP[0] > 0:
                remain_HP[0] = max(remain_HP[0] + dungeon[i][0], 0)
            else:
                remain_HP[0] = 0
                
            for j in xrange(1, len(remain_HP)):
                remain = 0
                if remain_HP[j - 1] > 0:
                    remain = max(remain_HP[j - 1] + dungeon[i][j], remain)
                if remain_HP[j] > 0:
                    remain = max(remain_HP[j] + dungeon[i][j], remain)
                remain_HP[j] = remain

        return remain_HP[-1] > 0