#!/usr/bin/env python2
# coding: utf-8
# file: FramesController.py

from flask import render_template
from flask import request
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app import web
from app.models import CobraWebFrame
from app.models import CobraWebFrameRules
from app.CommonClass.ValidateClass import login_required
from . import ADMIN_URL

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route(ADMIN_URL + "/frames", methods=["GET"])
@login_required
def show_all_frames():
    result = db.session.query(
        CobraWebFrame.frame_name, CobraWebFrame.description, CobraWebFrameRules.path_rule,
        CobraWebFrameRules.content_rule, CobraWebFrameRules.status, CobraWebFrameRules.id
    ).filter(CobraWebFrameRules.frame_id == CobraWebFrame.id).all()
    # print(result)
    return render_template("backend/frames/frames.html", data=dict(frames=result))


@web.route(ADMIN_URL + "/add_frame_rule", methods=["GET", "POST"])
@login_required
def add_frame_rule():

    if request.method == "POST":
        # print(request.form)
        status = request.form.get("status", 0)
        web_frame = request.form.get("web_frame", None)
        path_rule = request.form.get("path_rule", None)
        content_rule = request.form.get("content_rule", "")

        # 检查参数合法性
        if web_frame is None or web_frame == "" or not web_frame.isdigit():
            return jsonify(tag="danger", message="Web frame can't be blank.")
        if path_rule is None or path_rule == "":
            return jsonify(tag="danger", message="Path rule can't be blank.")
        web_frame_rule = CobraWebFrame.query.filter(CobraWebFrame.id == web_frame).all()
        if not len(web_frame_rule):
            return jsonify(tag="danger", message="No selected web frame.")

        # 插入数据
        web_frame_rule = CobraWebFrameRules(
            frame_id=web_frame, path_rule=path_rule, content_rule=content_rule, status=status
        )
        try:
            db.session.add(web_frame_rule)
            db.session.commit()
            return jsonify(tag="success", message="Add success.")
        except SQLAlchemyError as e:
            return jsonify(tag="warning", message=e)
    else:
        web_frames = db.session.query(
            CobraWebFrame.id, CobraWebFrame.frame_name, CobraWebFrame.description
        ).all()
        print(web_frames)
        return render_template("backend/frames/add_new_frame_rule.html", data=dict(frames=web_frames))


@web.route(ADMIN_URL + "/add_frame", methods=["GET", "POST"])
@login_required
def add_frame():

    if request.method == "POST":
        frame_name = request.form.get("frame_name", None)
        description = request.form.get("description", None)

        if frame_name is None or frame_name == "":
            return jsonify(tag="danger", message="Frame name can't be blank.")
        if description is None or description == "":
            return jsonify(tag="danger", message="Frame description can't be blank.")

        web_frame = CobraWebFrame(frame_name=frame_name, description=description)
        try:
            db.session.add(web_frame)
            db.session.commit()
            return jsonify(tag="success", message="Add Successful.")
        except SQLAlchemyError as e:
            return jsonify(tag="danger", message=e)

    else:
        return render_template("backend/frames/add_new_frame.html")
