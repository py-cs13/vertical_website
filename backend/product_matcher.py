#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品匹配器
根据AI分析结果匹配相关商品
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models import Product
import logging

logger = logging.getLogger(__name__)


class ProductMatcher:
    """商品匹配器，根据AI分析结果匹配相关商品"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def match_products(self, analysis_result: Dict[str, Any], limit: int = 2) -> List[Product]:
        """
        根据AI分析结果匹配商品
        
        Args:
            analysis_result: AI分析结果
            limit: 返回商品数量
            
        Returns:
            List[Product]: 匹配的商品列表
        """
        if not analysis_result:
            return []
        
        keywords = analysis_result.get("keywords", [])
        product_types = analysis_result.get("product_types", [])
        priority_categories = analysis_result.get("priority_categories", [])
        
        search_terms = keywords + product_types + priority_categories
        
        if not search_terms:
            return []
        
        products = self.db.query(Product).filter(
            Product.is_active == True
        ).all()
        
        scored_products = []
        for product in products:
            score = self._calculate_match_score(product, search_terms)
            if score > 0:
                scored_products.append((product, score))
        
        scored_products.sort(key=lambda x: x[1], reverse=True)
        matched_products = [product for product, score in scored_products[:limit]]
        
        logger.info(f"商品匹配完成: 搜索词={search_terms}, 匹配数={len(matched_products)}")
        return matched_products
    
    def _calculate_match_score(self, product: Product, search_terms: List[str]) -> float:
        """
        计算商品与搜索词的匹配分数
        
        Args:
            product: 商品对象
            search_terms: 搜索词列表
            
        Returns:
            float: 匹配分数
        """
        score = 0.0
        
        for term in search_terms:
            if term.lower() in product.name.lower():
                score += 10.0
        
        if product.description:
            for term in search_terms:
                if term.lower() in product.description.lower():
                    score += 5.0
        
        for term in search_terms:
            if term.lower() == product.category.lower():
                score += 8.0
        
        if hasattr(product, 'keywords') and product.keywords:
            keywords = product.keywords.split(",")
            for term in search_terms:
                if term.lower() in [k.lower().strip() for k in keywords]:
                    score += 3.0
        
        return score
