import os
import re

damping_factor = 0.85

def main():
    directory = 'corpus1'
    corpus = crawl(directory)
    transition_model(corpus, 'search.html', damping_factor)

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus. 
    """
    print("CURRENT PAGE")
    print(page)
    print("VALUE OF CORPUS[PAGE]")
    print(corpus[page])
    
    # find out probability distributions using iterative algorithm
    # PR(p) = 1-d/N + d*()
    
    # initialize a new dictionary to hold the probability distribution
    pages = list(corpus.keys())
    new_dict = {}
    
    for p in pages:
        new_dict[p] = 0
    
    # find the total pages in corpus to evenly distribute the possibility of each page being chosen randomly
    total_pages_in_corpus = len(corpus)

    probability_of_being_chosen_randomly = (1 - damping_factor)/total_pages_in_corpus

    # add the random probability of being chosen to each item in the dictionary
    for p in new_dict:
        new_dict[p] += probability_of_being_chosen_randomly
    
    
    # count the number of pages that the current page leads to
    number_of_pages = len(corpus[page])
    pages_of_interest = corpus[page]
    print("Pages that the current pages points to:", number_of_pages)

    link_following_possibility = damping_factor/number_of_pages
    
    for p in pages_of_interest:
        new_dict[p] += link_following_possibility
        
    
    return new_dict
         
if __name__=='__main__':
    main()