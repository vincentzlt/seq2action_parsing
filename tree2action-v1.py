
# coding: utf-8

# In[40]:


from pprint import pprint
from collections import namedtuple
import pickle


# In[41]:


word_info=namedtuple("word_info","id word pos head rel".split())


# In[42]:


data=pickle.load(open("./data.pkl","rb"))


# In[43]:


data[1]


# In[44]:


def shift(stack,buffer,actions):
    stack.append(buffer.pop(0))
    actions.append("shift")
    print("{:10} [{:>20}] [{:40}]".format("shift",
                                            " ".join([wi.word for wi in stack]),
                                            " ".join([wi.word for wi in buffer])))
    return stack,buffer,actions


# In[45]:


def swap(stack,buffer,actions):
    buffer.insert(0,stack.pop(-2))
    actions.append("swap")
    print("{:10} [{:>20}] [{:40}]".format("swap",
                                            " ".join([wi.word for wi in stack]),
                                            " ".join([wi.word for wi in buffer])))
    return stack,buffer,actions


# In[53]:


def left_r(stack,actions):
    
    _=stack.pop(-2)
    actions.append("left-reduce")
    print("{:15} [{:>20}] [{:40}]".format("left-r",
                                        " ".join([wi.word for wi in stack]),
                                        " ".join([wi.word for wi in buffer])))
    return stack,actions
    


# In[54]:


def right_r(stack,actions):
    
    _=stack.pop(-1)
    actions.append("right-reduce")
    print("{:15} [{:>20}] [{:40}]".format("right-r",
                                " ".join([wi.word for wi in stack]),
                                " ".join([wi.word for wi in buffer])))
    return stack,actions


# In[48]:


def swap_next_child(stack,buffer,actions,next_child_id):
    print("\nprocess non-proj swap {}".format(next_child_id))
    
    while stack[-1].id!=next_child_id:
        stack,buffer,actions=shift(stack,buffer,actions)
        
        
    while stack[-2].id!=stack[-1].head:
        stack,buffer,actions=swap(stack,buffer,actions)
    print("end process non-proj ...\n")
    return stack,buffer,actions


# In[49]:


def next_child(word,buffer):
    
    for wi in buffer:
        if wi.head==word.id:
            return wi.id
    return 0


# In[95]:


actions = []
outputs = []

for sent in data:
    stack = [word_info(-1, "ROOT", "ROOT", None, None)]
    buffer = sent[:]

    while len(buffer) > 0:
        if len(stack) == 1:
            stack, buffer, actions = shift(stack, buffer, actions)
        elif len(stack) == 2:
            next_child_id = next_child(stack[-1], buffer)
            #print(next_child_id)
            if next_child_id == buffer[0].id:
                stack, buffer, actions = shift(stack, buffer, actions)
                if next_child(stack[-1], buffer)==0:
                    stack, actions = right_r(stack, actions)
            elif next_child_id == 0:
                stack, buffer, actions = shift(stack, buffer, actions)
                if stack[-2].head == stack[-1].id:
                    stack, actions = left_r(stack, actions)
                elif stack[-2].id == stack[-1].head:
                    stack, actions = right_r(stack, actions)
            else:
                stack, buffer, actions = swap_next_child(
                    stack, buffer, actions, next_child_id)
        else:
            next_child_id = next_child(stack[-1], buffer)
            #print(next_child_id)

            if next_child_id == buffer[0].id:
                stack, buffer, actions = shift(stack, buffer, actions)
            elif next_child_id == 0:
                if stack[-2].head == stack[-1].id:
                    stack, actions = left_r(stack, actions)
                elif stack[-2].id == stack[-1].head:
                    stack, actions = right_r(stack, actions)
                else:
                    stack, buffer, actions = shift(stack, buffer, actions)
            else:
                stack, buffer, actions = swap_next_child(
                    stack, buffer, actions, next_child_id)
        #input()
        
    while len(stack)>1:
        if stack[-2].head == stack[-1].id:
                    stack, actions = left_r(stack, actions)
        elif stack[-2].id == stack[-1].head:
                    stack, actions = right_r(stack, actions)
        #input()
    outputs.append(actions)
    actions = []


# In[11]:


pickle.dump(outputs,open("parsing_sequences.pkl","wb"))

