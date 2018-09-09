# import aiohttp_jinja2
from aiohttp import web

import json


# @aiohttp_jinja2.template('index.html')
# async def index(request):
#     async with request.app['db'].acquire() as conn:
#         cursor = await conn.execute(db.question.select())
#         records = await cursor.fetchall()
#         questions = [dict(q) for q in records]
#         return {'questions': questions}


async def index(request):
    data = {'status': 'success'}
    return web.json_response(data, status=200)


async def new_user(request):
    try:
        # happy path where name is set
        user = request.query['name']
        # Process our new user
        print("Creating new user with name: ", user)

        data = {'status': 'success'}
        # return a success json response with status code 200 i.e. 'OK'
        return web.json_response(data, status=200)
    except Exception as e:
        # Bad path where name is not set
        data = {'status': 'failed', 'reason': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(data, status=500)

# @aiohttp_jinja2.template('detail.html')
# async def poll(request):
#     async with request.app['db'].acquire() as conn:
#         question_id = request.match_info['question_id']
#         try:
#             question, choices = await db.get_question(conn,
#                                                       question_id)
#         except db.RecordNotFound as e:
#             raise web.HTTPNotFound(text=str(e))
#         return {
#             'question': question,
#             'choices': choices
#         }


# @aiohttp_jinja2.template('results.html')
# async def results(request):
#     async with request.app['db'].acquire() as conn:
#         question_id = request.match_info['question_id']

#         try:
#             question, choices = await db.get_question(conn,
#                                                       question_id)
#         except db.RecordNotFound as e:
#             raise web.HTTPNotFound(text=str(e))

#         return {
#             'question': question,
#             'choices': choices
#         }


# async def vote(request):
#     async with request.app['db'].acquire() as conn:
#         question_id = int(request.match_info['question_id'])
#         data = await request.post()
#         try:
#             choice_id = int(data['choice'])
#         except (KeyError, TypeError, ValueError) as e:
#             raise web.HTTPBadRequest(
#                 text='You have not specified choice value') from e
#         try:
#             await db.vote(conn, question_id, choice_id)
#         except db.RecordNotFound as e:
#             raise web.HTTPNotFound(text=str(e))
#         router = request.app.router
#         url = router['results'].url_for(question_id=str(question_id))
#         return web.HTTPFound(location=url)
