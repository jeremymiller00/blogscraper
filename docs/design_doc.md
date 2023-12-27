# Blog Scraper Design Docs

## Goal: avoid manual scraping (copy-paste) of blogs that I want to include in my Data Science Library
### Secondary Goal: get experience making a project; have fun

Input: blog to follow
Output: regular scraping of new content and adding it to ds library

## User Story:
As a Product Manager, I want to input the start page (archive page? list of all articles?) of a blog and have the helper automatically scrape that content into Markdown files in my Data Science Vault so that I can automate the building of my library of trusted content.

## Requirements
Connectors for 
* Substack (Simon Willison, Eugene Yan, John Cutler, Katie Bauer)
* Lenny's Podcast for transcripts
* Chip Huyen

## Once the base page is identified (article archive), all work is automated to
* Scrape the article (probably want to do at midnight or something)
* Create the md file in the vault
* Send me an email telling me it was done, and reminding me to gitupdate the vault (can I automate the triggering of this script?)
* Smart Connections plugin will then automatically index and store vectors

## Provide abstractions for:
Add new start page of blog
Update start page of blog
List which pages have been scraped for a given blog
Create a report of activity in the last N days

Handle content other than blogs?
Online PDF?

## System Design
* A specific blog gets in own bot
* All inherit from base bot
* A database (file? sqlite?) is needed to track what has been scraped
 * Just a json file for now
* Get list of pages, filter, then scrape
* Or go by last scraping date, get since then

# Objects
## BaseBot
read_database
update_database
get_blog_pages
scrape_pages
scrape_page
update_scraped_status

## SubstackBot
get_blog_pages
scrape_page

## Language Model
generate (generic function)
generate_local
generate_gpt
clean_blog
prepare_text
get_model
set_model

Based on the following design document, write a Python application: