
# coding: utf-8

# In[21]:


from pprint import pprint
from collections import namedtuple


# In[2]:


train_file="./toy_train.txt"


# In[23]:


word_info=namedtuple("word_info","id word pos head rel".split())


# In[24]:


data=[]
sentence=[]

for line in open(train_file,"r",encoding="utf-8"):
    line=line[:-1]
    
    if len(line)!=0:
        ID,word,base, pos, pos1,_,head,rel=line.split("\t")
        ID=int(ID)-1
        head=int(head)-1
        
        sentence.append(word_info(ID,word,pos,head,rel))
    else:
        data.append(sentence)
        sentence=[]
        


# In[26]:


pprint(data)


# In[37]:


actions=[]

for sent in data:
    stack=[word_info(-1,"ROOT","ROOT",None,None)]
    buffer=sent[:]
    while len(buffer)>0 and len(stack)>1:
        stack.append(buffer.pop[0])
        actions.append("shift")
        print("{:15} [{:>20}] [{:40}]".format("shift",
                                            " ".join([wi.word for wi in stack]),
                                            " ".join([wi.word for wi in buffer])))
        
        next_child_id=next_child(stack[-1],buffer)
        
        if next_child_id:
            stack,buffer,actions=swap_next_child(stack,buffer,actions,next_child_id)
        
        while len(buffer)>2:
            if stack[-1].head==stack[-2].id:
                stack.pop(-1)
                actions.append("right-reduce")
                print("{:15} [{:>20}] [{:40}]".format("right-reduce",
                                            " ".join([wi.word for wi in stack]),
                                            " ".join([wi.word for wi in buffer])))
            elif stack[-2].head==stack[-1].id:
                stack.pop(-2)
                actions.append("left-reduce")
                print("{:15} [{:>20}] [{:40}]".format("left-reduce",
                                            " ".join([wi.word for wi in stack]),
                                            " ".join([wi.word for wi in buffer])))
            else:
                break
            
        


# In[36]:


def swap_next_child(stack,buffer,actions,next_child_id):
    while stack[-1].id!=next_child_id:
        stack.append(buffer.pop(0))
        actions.append("shift")
        print("{:15} [{:>20}] [{:40}]".format("shift",
                                            " ".join([wi.word for wi in stack]),
                                            " ".join([wi.word for wi in buffer])))
    while stack[-2].id!=stack[-1].head:
        buffer.insert(0,stack.pop(-2))
        actions.append("swap")
        print("{:15} [{:>20}] [{:40}]".format("swap",
                                            " ".join([wi.word for wi in stack]),
                                            " ".join([wi.word for wi in buffer])))
    return stack,buffer,actions


# In[30]:


def next_child(word,buffer):
    for wi in buffer:
        if wi.head==word.id:
            return wi.id
    return 0


# In[34]:


list(range(1,5)).pop(-2)


# In[ ]:




