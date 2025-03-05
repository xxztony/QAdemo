from enum import Enum


class LocateBy(Enum):
    """
    Element Locator Types for UI Automation

    Defines the supported locator types for finding elements in the UI automation framework.
    Supports both Android and iOS platforms with their respective locator strategies.

    Available locator types:
    - ID: Locate element by resource-id (Android) or accessibility identifier (iOS)
    - XPATH: Locate element using XPath expression
    - TEXT: Locate element by exact text match
    - TEXT_CONTAINS: Locate element by partial text match
    - IOS_PREDICATE: iOS-specific NSPredicate locator
    - IOS_CLASS_CHAIN: iOS-specific Class Chain locator
    - ACCESSIBILITY_ID: Cross-platform accessibility identifier
    """
    ID = "id"  # Resource ID locator
    XPATH = "xpath"  # XPath expression locator
    TEXT = "text"  # Exact text match locator
    TEXT_CONTAINS = "text_contains"  # Partial text match locator
    IOS_PREDICATE = "ios_predicate"  # iOS NSPredicate locator
    IOS_CLASS_CHAIN = "ios_class_chain"  # iOS Class Chain locator
    ACCESSIBILITY_ID = "accessibility_id"  # Accessibility identifier locator
