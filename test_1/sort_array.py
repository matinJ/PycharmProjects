__author__ = 'Jian'

def bubble_sort(bubblelist):
    alen = len(bubblelist)
    while alen>0:
        for i in range(alen -1):
            if bubblelist[i]>bubblelist[i+1]:
                bubblelist[i]=bubblelist[i]+bubblelist[i+1]
                bubblelist[i+1]=bubblelist[i]-bubblelist[i+1]
                bubblelist[i]=bubblelist[i]-bubblelist[i+1]
        alen -=1
    print bubblelist

if __name__ == '__main__':
    bubblelist=[3,4,1,2,5,8,0]
    bubble_sort(bubblelist)


