# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from config import CONFIG_DEBUG
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required,current_user
from json import dumps,loads
from .. import models
from ..utils import *
from ..conf.config import *
from . import novel
@novel.route("/")
@novel.route("/<int:page>")
def index(page=1):
    try:
        items = models.Novel.select()\
            .order_by(models.Novel.update_time)\
            .paginate(page, 20)
    except Exception as e:
        return jsonresp({
            "code": -4,
            "msg": "内部错误",
            "error": str(e) if CONFIG_DEBUG else ""
        })
    result = query_to_list(items)
    return jsonresp({
        "code": 0,
        "msg": "成功。",
        "data": {"novel": result}
    })
@novel.route("/api/novel/detail/<int:nid>")
def detail(nid=0):
    if nid ==0:
        return jsonresp({"code": -2, "msg": "缺少参数"})
    try:
        items = models.Novel.get(models.Novel.id == nid)
    except Exception as e:
        return jsonresp({
            "code": -4,
            "msg": "内部错误",
            "error": str(e) if CONFIG_DEBUG else ""
        })
    result = query_to_list(items)[0]
    return jsonresp({
        "code": 0,
        "msg": "成功。",
        "data": {"novel": result}
    })
@novel.route("/search/<text>")
@novel.route("/search/<text>/<int:page>")
def search(text="",page=1 ):
    inprofile = request.args.get("inprofile")
    if not text:
        return jsonresp({"code": -2, "msg": "缺少参数"})
    try:
        if inprofile:
            items = models.Novel\
                .select()\
                .where(
                models.Novel.title ** "%"+text+"%"
                and models.Novel.description ** "%"+text+"%"
            ).paginate(page, 20)
        else:
            items = models.Novel \
                .select() \
                .where(
                models.Novel.title ** "%" + text + "%"
            ).paginate(page, 20)
    except Exception as e:
        return jsonresp({
            "code": -4,
            "msg": "内部错误",
            "error": str(e) if CONFIG_DEBUG else ""
        })
    result = query_to_list(items)
    return jsonresp({
        "code": 0,
        "msg": "成功。",
        "data": {"novel": result}
    })
@novel.route("/volumes/<int:nid>")
@novel.route("/volumes/<int:nid>/<int:page>")
def volumes(nid=0,page=1):
    if nid ==0:
        return jsonresp({"code": -2, "msg": "缺少参数"})
    try:
        items = models.Novel.get(models.Novel.id == nid).volumes
        items = loads(items)
        results = []
        for i in items:
            obj =models.Volume.get(models.Volume.id == i)
            results.append({
                "vid":obj.vid,
                "title":obj.title,
                "chapters":obj.chapters,
                "update_time":obj.update_time
            })
    except Exception as e:
        return jsonresp({
            "code": -4,
            "msg": "内部错误",
            "error": str(e) if CONFIG_DEBUG else ""
        })
    return jsonresp({"code": 0, "msg": "成功","data":{"novel":results}})
@novel.route("/author/<name>")
def author(name=""):
    if not name:
        return jsonresp({"code": -2, "msg": "缺少参数"})
    try:
        items = models.Novel.select().where(
            models.Novel.author == name
        ).paginate(page, 20)
    except Exception as e:
        return jsonresp({
            "code": -4,
            "msg": "内部错误",
            "error": str(e) if CONFIG_DEBUG else ""
        })
    result = query_to_list(items)
    return jsonresp({
        "code": 0,
        "msg": "成功。",
        "data": {"novel": result}
    })

@novel.route("/subscribe/<nid>")
@login_required
def subscribe(nid):
    if not nid:
        return jsonresp({"code": -2, "msg": "缺少参数"})
    try:
        models.NovelSubscribe.create(novel=nid,user=current_user.id)
    except Exception as e:
        return jsonresp({
            "code": -4,
            "msg": "内部错误",
            "error": str(e) if CONFIG_DEBUG else ""
        })
    return jsonresp({
        "code": 0,
        "msg": "成功。"
    })